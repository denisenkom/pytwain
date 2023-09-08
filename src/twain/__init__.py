import logging
import os
import ctypes as ct
import sys
import typing
import weakref
from . import windows
from . import utils
from .exceptions import *
from .lowlevel.constants import *
from .lowlevel.structs import *

logger = logging.getLogger('lowlevel')

_exc_mapping = {TWCC_SUCCESS: excTWCC_SUCCESS,
                TWCC_BUMMER: excTWCC_BUMMER,
                TWCC_LOWMEMORY: MemoryError,
                TWCC_NODS: excTWCC_NODS,
                TWCC_OPERATIONERROR: excTWCC_OPERATIONERROR,
                TWCC_BADCAP: excTWCC_BADCAP,
                TWCC_BADPROTOCOL: excTWCC_BADPROTOCOL,
                TWCC_BADVALUE: ValueError,
                TWCC_SEQERROR: excTWCC_SEQERROR,
                TWCC_BADDEST: excTWCC_BADDEST,
                TWCC_CAPUNSUPPORTED: excTWCC_CAPUNSUPPORTED,
                TWCC_CAPBADOPERATION: excTWCC_CAPBADOPERATION,
                TWCC_CAPSEQERROR: excTWCC_CAPSEQERROR,
                TWCC_DENIED: excTWCC_DENIED,
                TWCC_FILEEXISTS: excTWCC_FILEEXISTS,
                TWCC_FILENOTFOUND: excTWCC_FILENOTFOUND,
                TWCC_NOTEMPTY: excTWCC_NOTEMPTY,
                TWCC_PAPERJAM: excTWCC_PAPERJAM,
                TWCC_PAPERDOUBLEFEED: excTWCC_PAPERDOUBLEFEED,
                TWCC_FILEWRITEERROR: excTWCC_FILEWRITEERROR,
                TWCC_CHECKDEVICEONLINE: excTWCC_CHECKDEVICEONLINE}

_ext_to_type = {'.bmp': TWFF_BMP,
                '.jpg': TWFF_JFIF,
                '.jpeg': TWFF_JFIF,
                '.png': TWFF_PNG,
                '.tiff': TWFF_TIFF,
                '.tif': TWFF_TIFF,
                }

_mapping = {TWTY_INT8: ct.c_int8,
            TWTY_UINT8: ct.c_uint8,
            TWTY_INT16: ct.c_int16,
            TWTY_UINT16: ct.c_uint16,
            TWTY_UINT32: ct.c_uint32,
            TWTY_INT32: ct.c_int32,
            TWTY_BOOL: ct.c_uint16,
            TWTY_FIX32: TW_FIX32,
            TWTY_FRAME: TW_FRAME,
            TWTY_STR32: ct.c_char * 34,
            TWTY_STR64: ct.c_char * 66,
            TWTY_STR128: ct.c_char * 130,
            TWTY_STR255: ct.c_char * 255}


def _is_good_type(type_id: int) -> bool:
    return type_id in list(_mapping.keys())


def _struct2dict(struct, decode) -> dict[str, typing.Any]:
    result = {}
    for field, _ in struct._fields_:
        value = getattr(struct, field)
        if hasattr(value, "_length_") and hasattr(value, "_type_"):
            # Probably an array
            value = list(value)
        elif hasattr(value, "_fields_"):
            # Probably another struct
            value = _struct2dict(value, decode)
        if isinstance(value, bytes):
            value = decode(value)
        result[field] = value
    return result


if utils.is_windows():
    def _twain1_alloc(size: int) -> ct.c_void_p:
        return windows.GlobalAlloc(windows.GMEM_ZEROINIT, size)


    _twain1_free = windows.GlobalFree
    _twain1_lock = windows.GlobalLock
    _twain1_unlock = windows.GlobalUnlock
else:
    # Mac
    def _twain1_alloc(size: int) -> ct.c_void_p:
        return ct.libc.malloc(size)


    def _twain1_lock(handle):
        return handle


    def _twain1_unlock(handle):
        pass


    def _twain1_free(handle):
        return ct.libc.free(handle)


class _Image(object):
    def __init__(self, handle):
        self._handle = handle

    def __del__(self):
        self.close()

    def close(self):
        """Releases memory of image"""
        self._free(self._handle)
        self._handle = None

    def save(self, filepath: str):
        """Saves in-memory image to BMP file"""
        windows.dib_write(self._handle, filepath, self._lock, self._unlock)


class Source(object):
    """
    This object represents connection to Data Source.

    An instance of this class can be created by calling
    :meth:`SourceManager.open_source`
    """

    def __init__(self, sm, ds_id: TW_IDENTITY):
        self._sm = sm
        self._id = ds_id
        self._state = 'open'
        self._version2 = bool(ds_id.SupportedGroups & DF_DS2)
        if self._version2:
            self._alloc = sm._alloc
            self._free = sm._free
            self._lock = sm._lock
            self._unlock = sm._unlock
            self._encode = sm._encode
            self._decode = sm._decode
        else:
            self._alloc = _twain1_alloc
            self._free = _twain1_free
            self._lock = _twain1_lock
            self._unlock = _twain1_unlock
            self._encoding = sys.getfilesystemencoding()
            self._encode = lambda s: s.encode(self._encoding)
            self._decode = lambda s: s.decode(self._encoding)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """This method is used to close the data source object.
        It gives finer control over this connects than relying on garbage collection.
        """
        if self._state == 'ready':
            self._end_all_xfers()
        if self._state == 'enabled':
            self._disable()
        if self._state == 'open':
            self._sm._close_ds(self._id)
            self._state = 'closed'
            self._sm = None

    def _call(self, dg: int, dat: int, msg: int, buf, expected_returns=(TWRC_SUCCESS,)) -> int:
        return self._sm._call(self._id, dg, dat, msg, buf, expected_returns)

    def _get_capability(self, cap: int, current: int):
        twCapability = TW_CAPABILITY(cap, TWON_DONTCARE16, 0)
        self._call(DG_CONTROL, DAT_CAPABILITY, current, ct.byref(twCapability))
        try:
            ptr = self._lock(twCapability.hContainer)
            try:
                if twCapability.ConType == TWON_ONEVALUE:
                    type_id = int(ct.cast(ptr, ct.POINTER(ct.c_uint16))[0])
                    if not _is_good_type(type_id):
                        msg = "Capability Code = %d, Format Code = %d, Item Type = %d" % (cap,
                                                                                          twCapability.ConType,
                                                                                          type_id)
                        raise excCapabilityFormatNotSupported(msg)
                    ctype = _mapping.get(type_id)
                    val = ct.cast(ptr + 2, ct.POINTER(ctype))[0]
                    if type_id in (TWTY_INT8, TWTY_UINT8, TWTY_INT16, TWTY_UINT16, TWTY_UINT32, TWTY_INT32):
                        pass
                    elif type_id == TWTY_BOOL:
                        val = bool(val)
                    elif type_id == TWTY_FIX32:
                        val = fix2float(val)
                    elif type_id == TWTY_FRAME:
                        val = frame2tuple(val)
                    return type_id, val
                elif twCapability.ConType == TWON_RANGE:
                    rng = ct.cast(ptr, ct.POINTER(TW_RANGE)).contents
                    return {'MinValue': rng.MinValue,
                            'MaxValue': rng.MaxValue,
                            'StepSize': rng.StepSize,
                            'DefaultValue': rng.DefaultValue,
                            'CurrentValue': rng.CurrentValue}
                elif twCapability.ConType == TWON_ENUMERATION:
                    enum = ct.cast(ptr, ct.POINTER(TW_ENUMERATION)).contents
                    if not _is_good_type(enum.ItemType):
                        msg = "Capability Code = %d, Format Code = %d, Item Type = %d" % (cap,
                                                                                          twCapability.ConType,
                                                                                          enum.ItemType)
                        raise excCapabilityFormatNotSupported(msg)
                    ctype = _mapping[enum.ItemType]
                    item_p = ct.cast(ptr + ct.sizeof(TW_ENUMERATION), ct.POINTER(ctype))
                    values = [el for el in item_p[0:enum.NumItems]]
                    return enum.ItemType, (enum.CurrentIndex, enum.DefaultIndex, values)
                elif twCapability.ConType == TWON_ARRAY:
                    arr = ct.cast(ptr, ct.POINTER(TW_ARRAY)).contents
                    if not _is_good_type(arr.ItemType):
                        msg = "Capability Code = %d, Format Code = %d, Item Type = %d" % (cap,
                                                                                          twCapability.ConType,
                                                                                          arr.ItemType)
                        raise excCapabilityFormatNotSupported(msg)
                    ctype = _mapping[arr.ItemType]
                    item_p = ct.cast(ptr + ct.sizeof(TW_ARRAY), ct.POINTER(ctype))
                    return arr.ItemType, [el for el in item_p[0:arr.NumItems]]
                else:
                    msg = "Capability Code = %d, Format Code = %d" % (cap, twCapability.ConType)
                    raise excCapabilityFormatNotSupported(msg)
            finally:
                self._unlock(twCapability.hContainer)
        finally:
            self._free(twCapability.hContainer)

    def get_capability(self, cap: int):
        """This function is used to return the capability information from the source.
        If the capability is not supported, an exception should be returned.
        Capabilities are returned as a tuple of a type (TWTY_*) and a value.
        The format of values depends on their container type.
        Capabilities can be in any of the following containers:
            singleton, range, enumerator or array.

         singletons are returned as a single value (integer or string)
         ranges are returned as a tuple dictionary containing MinValue,
             MaxValue, StepSize, DefaultValue and CurrentValue
         enumerators and arrays are returned as tuples, each containing
             a list which has the actual values
        """
        return self._get_capability(cap, MSG_GET)

    def get_capability_current(self, cap: int):
        """This function is used to return the current value of a capability from the source.
        If the capability is not supported, an exception should be returned.
        Capabilities are returned as a tuple of a type (TWTY_*) and a value.
        The format of values depends on their container type.
        Capabilities can be in any of the following containers:
            singleton, range, enumerator or array.

         singletons are returned as a single value (integer or string)
         ranges are returned as a tuple dictionary containing MinValue,
             MaxValue, StepSize, DefaultValue and CurrentValue
         enumerators and arrays are returned as tuples, each containing
             a list which has the actual values
        """
        return self._get_capability(cap, MSG_GETCURRENT)

    def get_capability_default(self, cap: int):
        """This function is used to return the default value of a capability from the source.
        If the capability is not supported, an exception should be returned.
        Capabilities are returned as a tuple of a type (TWTY_*) and a value.
        The format of values depends on their container type.
        Capabilities can be in any of the following containers:
            singleton, range, enumerator or array.

         singletons are returned as a single value (integer or string)
         ranges are returned as a tuple dictionary containing MinValue,
             MaxValue, StepSize, DefaultValue and CurrentValue
         enumerators and arrays are returned as tuples, each containing
             a list which has the actual values
        """
        return self._get_capability(cap, MSG_GETDEFAULT)

    @property
    def name(self) -> str:
        """Get the name of the source. This can be used later for
        connecting to the same source.
        """
        return self._decode(self._id.ProductName)

    @property
    def identity(self) -> dict:
        """This function is used to retrieve information about the source.
        driver. The information is returned in a dictionary.
        """
        res = _struct2dict(self._id, self._decode)
        res.update(_struct2dict(self._id.Version, self._decode))
        return res

    def set_capability(self, cap: int, type_id: int, value: int | float | tuple):
        """This function is used to set the value of a capability in the source.
        Three parameters are required, a Capability Identifier (lowlevel.CAP_* or
        lowlevel.ICAP_*) a value type (lowlevel.TWTY_*) and a value
        If the capability is not supported, an exception should be returned.
        This function is used to set a value using a TW_ONEVALUE.
        """
        if not _is_good_type(type_id):
            raise excCapabilityFormatNotSupported("Capability Code = %d, Format Code = %d" % (cap, type_id))
        ctype = _mapping[type_id]
        if type_id in (TWTY_INT8, TWTY_INT16, TWTY_INT32, TWTY_UINT8, TWTY_UINT16, TWTY_UINT32, TWTY_BOOL):
            cval = ctype(value)
        elif type_id in (TWTY_STR32, TWTY_STR64, TWTY_STR128, TWTY_STR255):
            cval = ctype(self._encode(value))
        elif type_id == TWTY_FIX32:
            cval = float2fix(value)
        elif type_id == TWTY_FRAME:
            cval = tuple2frame(value)
        else:
            assert 0, 'invalid case'
        handle = self._alloc(ct.sizeof(TW_ONEVALUE) + ct.sizeof(ctype))
        try:
            ptr = self._lock(handle)
            try:
                ct.cast(ptr, ct.POINTER(ct.c_uint16))[0] = type_id
                ct.cast(ptr + 2, ct.POINTER(ctype))[0] = cval
            finally:
                self._unlock(handle)
            capability = TW_CAPABILITY(cap, TWON_ONEVALUE, handle)
            rv = self._call(DG_CONTROL,
                            DAT_CAPABILITY,
                            MSG_SET,
                            ct.byref(capability),
                            [TWRC_CHECKSTATUS])
        finally:
            self._free(handle)
        if rv == TWRC_CHECKSTATUS:
            raise CheckStatus

    def reset_capability(self, cap: int):
        """This function is used to reset the value of a capability to the source default.

        :param cap: Capability Identifier (lowlevel.CAP_* or lowlevel.ICAP_*).
        """
        cap = TW_CAPABILITY(Cap=cap)
        self._call(DG_CONTROL, DAT_CAPABILITY, MSG_RESET, ct.byref(cap))

    def set_image_layout(self, frame: tuple[float, float, float, float], document_number: int = 1, page_number: int = 1, frame_number: int = 1):
        """This function is used to inform the source of the Image Layout.

        It uses a tuple containing frame coordinates, document
        number, page number, frame number.
        """
        il = TW_IMAGELAYOUT(Frame=tuple2frame(frame),
                            DocumentNumber=document_number,
                            PageNumber=page_number,
                            FrameNumber=frame_number)
        rv = self._call(DG_IMAGE,
                        DAT_IMAGELAYOUT,
                        MSG_SET,
                        ct.byref(il),
                        (TWRC_SUCCESS, TWRC_CHECKSTATUS))
        if rv == TWRC_CHECKSTATUS:
            raise CheckStatus

    def get_image_layout(self) -> tuple[tuple[float, float, float, float], int, int, int]:
        """This function is used to ask the source for Image Layout.

        It returns a tuple containing frame coordinates, document
        number, page number, frame number.

        Valid states 4 through 6
        """
        il = TW_IMAGELAYOUT()
        self._call(DG_IMAGE, DAT_IMAGELAYOUT, MSG_GET, ct.byref(il))
        return frame2tuple(il.Frame), il.DocumentNumber, il.PageNumber, il.FrameNumber

    def get_image_layout_default(self) -> tuple[tuple[float, float, float, float], int, int, int]:
        """This function is used to ask the source for default Image Layout.

        It returns a tuple containing frame coordinates, document
        number, page number, frame number.

        Valid states 4 through 6
        """
        il = TW_IMAGELAYOUT()
        self._call(DG_IMAGE, DAT_IMAGELAYOUT, MSG_GETDEFAULT, ct.byref(il))
        return frame2tuple(il.Frame), il.DocumentNumber, il.PageNumber, il.FrameNumber

    def reset_image_layout(self):
        """This function is used to reset Image Layout to its default settings"""
        il = TW_IMAGELAYOUT()
        self._call(DG_IMAGE, DAT_IMAGELAYOUT, MSG_RESET, ct.byref(il))

    def _enable(self, show_ui: bool, modal_ui: bool, hparent):
        """This function is used to ask the source to begin aquistion.
        Parameters:
            show_ui - bool
            modal_ui - bool
        """
        ui = TW_USERINTERFACE(ShowUI=show_ui, ModalUI=modal_ui, hParent=hparent)
        logger.info("starting scan")
        self._call(DG_CONTROL, DAT_USERINTERFACE, MSG_ENABLEDS, ct.byref(ui))
        self._state = 'enabled'

    def _disable(self):
        """This function is used to ask the source to hide the user interface."""
        ui = TW_USERINTERFACE()
        self._call(DG_CONTROL, DAT_USERINTERFACE, MSG_DISABLEDS, ct.byref(ui))
        self._state = 'open'

    def _process_event(self, msg_ref) -> tuple[int, int]:
        """The TWAIN interface requires that the windows events
        are available to both the application and the lowlevel
        source (which operates in the same process).
        This method is called in the event loop to pass on those
        events.
        """
        event = TW_EVENT(ct.cast(msg_ref, ct.c_void_p), 0)
        rv = self._call(DG_CONTROL,
                        DAT_EVENT,
                        MSG_PROCESSEVENT,
                        ct.byref(event),
                        (TWRC_DSEVENT,
                         TWRC_NOTDSEVENT))
        logger.debug("handling event result %d", rv)
        if event.TWMessage == MSG_XFERREADY:
            logger.info("transfer is ready")
            self._state = 'ready'
        return rv, event.TWMessage

    def _modal_loop(self, callback: typing.Callable[[int], None]):
        logger.info("entering modal loop")
        done = False
        msg = MSG()
        while not done:
            if not windows.GetMessage(ct.byref(msg), 0, 0, 0):
                break
            rc, event = self._process_event(ct.byref(msg))
            if rc not in (TWRC_NOTDSEVENT, TWRC_DSEVENT):
                logger.info("got unusual process event result %d", rc)
            if callback:
                callback(event)
            if event in (MSG_XFERREADY, MSG_CLOSEDSREQ):
                done = True
            if rc == TWRC_NOTDSEVENT:
                windows.TranslateMessage(ct.byref(msg))
                windows.DispatchMessage(ct.byref(msg))
        logger.info("exited modal loop")

    def _acquire(self, callback: typing.Callable[[], int], show_ui: bool = True, modal: bool = False):
        self._enable(show_ui, modal, self._sm._hwnd)
        try:
            def callback_lolevel(event: int):
                if event == MSG_XFERREADY:
                    logger.info("got MSG_XFERREADY message")
                    more = True
                    while more:
                        try:
                            more = callback()
                        except CancelAll:
                            self._end_all_xfers()
                            break

            self._modal_loop(callback_lolevel)
        finally:
            self._disable()

    @property
    def file_xfer_params(self) -> tuple[str, int]:
        """ Property which stores tuple of (file name, format) where format is one of TWFF_*

        This property is used by :meth:`xfer_image_by_file`

        Valid states: 4, 5, 6
        """
        sfx = TW_SETUPFILEXFER()
        self._call(DG_CONTROL, DAT_SETUPFILEXFER, MSG_GET, ct.byref(sfx))
        return self._decode(sfx.FileName), sfx.Format

    @file_xfer_params.setter
    def file_xfer_params(self, params: tuple[str, int]):
        (path, fmt) = params
        sfx = TW_SETUPFILEXFER(self._encode(path), fmt, 0)
        self._call(DG_CONTROL, DAT_SETUPFILEXFER, MSG_SET, ct.byref(sfx))

    @property
    def image_info(self) -> dict:
        """This function is used to ask the source for Image Info.
        Normally, the application is notified that the image is
        ready for transfer using the message loop. However, it is
        hard to get at the message loop in toolkits such as wxPython.
        As an alternative, I poll the source looking for image information.
        When the image information is available, the image is ready for transfer

        Valid states: 6, 7
        """
        ii = TW_IMAGEINFO()
        self._call(DG_IMAGE,
                   DAT_IMAGEINFO,
                   MSG_GET,
                   ct.byref(ii))
        return {"XResolution": fix2float(ii.XResolution),
                "YResolution": fix2float(ii.YResolution),
                "ImageWidth": ii.ImageWidth,
                "ImageLength": ii.ImageLength,
                "SamplesPerPixel": ii.SamplesPerPixel,
                "BitsPerSample": list(ii.BitsPerSample),
                "BitsPerPixel": ii.BitsPerPixel,
                "Planar": ii.Planar,
                "PixelType": ii.PixelType,
                "Compression": ii.Compression}

    def _get_native_image(self) -> [int, ct.c_void_p]:
        hbitmap = ct.c_void_p()
        rv = self._call(DG_IMAGE,
                        DAT_IMAGENATIVEXFER,
                        MSG_GET,
                        ct.byref(hbitmap),
                        (TWRC_XFERDONE, TWRC_CANCEL))
        return rv, hbitmap

    def _get_file_image(self) -> int:
        return self._call(DG_IMAGE,
                          DAT_IMAGEFILEXFER,
                          MSG_GET,
                          None,
                          (TWRC_XFERDONE, TWRC_CANCEL))

    def _get_file_audio(self) -> int:
        return self._call(DG_AUDIO,
                          DAT_AUDIOFILEXFER,
                          MSG_GET,
                          None,
                          (TWRC_XFERDONE, TWRC_CANCEL))

    def _end_xfer(self) -> int:
        px = TW_PENDINGXFERS()
        self._call(DG_CONTROL, DAT_PENDINGXFERS, MSG_ENDXFER, ct.byref(px))
        if px.Count == 0:
            self._state = 'enabled'
        return px.Count

    def _end_all_xfers(self):
        """Cancel all outstanding transfers on the data source."""
        px = TW_PENDINGXFERS()
        self._call(DG_CONTROL, DAT_PENDINGXFERS, MSG_RESET, ct.byref(px))
        self._state = 'enabled'

    def request_acquire(self, show_ui: bool, modal_ui: bool):
        """This function is used to ask the source to begin acquisition.

        Transitions Source to state 5.

        :param show_ui: bool (default 1)
        :param modal_ui: bool (default 1)

        Valid states: 4
        """
        self._enable(show_ui, modal_ui, self._sm._hwnd)

    def modal_loop(self):
        """This function should be called after call to :func:`requiest_acquire`
        it will return after acquisition complete.

        Valid states: 5
        """
        self._modal_loop(self._sm._cb)

    def hide_ui(self):
        """This function is used to ask the source to hide the user interface.

        Transitions Source to state 4 if successful.

        Valid states: 5
        """
        self._disable()

    def xfer_image_natively(self) -> tuple[typing.Any, int]:
        """Perform a 'Native' form transfer of the image.

        When successful, this routine returns two values,
        an image handle and a count of the number of images
        remaining in the source.

        If remaining number of images is zero Source will
        transition to state 5, otherwise it stays in state 6
        in which case you should call
        :meth:`xfer_image_natively` again.

        Valid states: 6
        """
        rv, handle = self._get_native_image()
        more = self._end_xfer()
        if rv == TWRC_CANCEL:
            raise excDSTransferCancelled
        return handle.value, more

    def xfer_image_by_file(self) -> int:
        """Perform a file based transfer of the image.

        When successful, the file is saved to the image file,
        defined in a previous call to :meth:`file_xfer_params`.

        Returns the number of pending transfers

        If remaining number of images is zero Source will
        transition to state 5, otherwise it stays in state 6
        in which case you should call
        :meth:`xfer_image_natively` again.

        Valid states: 6
        """
        rv = self._get_file_image()
        more = self._end_xfer()
        if rv == TWRC_CANCEL:
            raise excDSTransferCancelled
        return more

    def acquire_file(self, before: typing.Callable[[dict], str], after: typing.Callable[[int], None] = lambda more: None, show_ui: bool = True, modal: bool = False):
        """Acquires one or more images as files. Call returns when acquisition complete.

        :param before: Callback called before each acquired file, it should return
                       full file path. It can also throw CancelAll to cancel acquisition
        :keyword after: Callback called after each acquired file, it receives number of
                        images remaining. It can throw CancelAll to cancel remaining
                        acquisition
        :keyword show_ui: If True source's UI will be presented to user
        :keyword modal: If True source's UI will be modal
        """
        _, (_, _, mechs) = self.get_capability(ICAP_XFERMECH)
        if TWSX_FILE not in mechs:
            raise Exception('File transfer is not supported')

        def callback():
            filepath = before(self.image_info)
            import os
            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            if ext != '.bmp':
                import tempfile
                handle, bmppath = tempfile.mkstemp('.bmp')
                os.close(handle)
            else:
                bmppath = filepath

            self.file_xfer_params = bmppath, TWFF_BMP
            rv = self._get_file_image()
            more = self._end_xfer()
            if rv == TWRC_CANCEL:
                raise excDSTransferCancelled
            if ext != '.bmp':
                try:
                    import Image
                except ImportError:
                    from PIL import Image
                Image.open(bmppath).save(filepath)
                os.remove(bmppath)
            after(more)
            return more

        self.set_capability(ICAP_XFERMECH, TWTY_UINT16, TWSX_FILE)
        self._acquire(callback, show_ui, modal)

    def acquire_natively(self, after: typing.Callable[[_Image, int], None], before: typing.Callable[[dict], str] = lambda img_info: None, show_ui: bool = True, modal: bool = False):
        """Acquires one or more images in memory. Call returns when acquisition complete

        :param after: Callback called after each acquired file, it receives an image object and
                     number of images remaining. It can throw CancelAll to cancel remaining
                     acquisition
        :keyword before: Callback called before each acquired file. It can throw CancelAll
                      to cancel acquisition
        :keyword show_ui: If True source's UI will be presented to user
        :keyword modal:   If True source's UI will be modal
        """

        def callback() -> int:
            before(self.image_info)
            rv, handle = self._get_native_image()
            more = self._end_xfer()
            if rv == TWRC_CANCEL:
                raise excDSTransferCancelled
            after(_Image(handle), more)
            return more

        self.set_capability(ICAP_XFERMECH, TWTY_UINT16, TWSX_NATIVE)
        self._acquire(callback, show_ui, modal)

    def is_twain2(self):
        return self._version2

    # backward compatible aliases
    def destroy(self):
        self.close()

    def GetCapabilityCurrent(self, cap):
        warnings.warn("GetCapabilityCurrent is deprecated, use get_capability_current instead", DeprecationWarning)
        return self.get_capability_current(cap)

    def GetCapabilityDefault(self, cap):
        warnings.warn("GetCapabilityDefault is deprecated, use get_capability_default instead", DeprecationWarning)
        return self.get_capability_default(cap)

    def GetSourceName(self):
        warnings.warn("GetSourceName is deprecated, use name property instead", DeprecationWarning)
        return self.name

    def GetIdentity(self):
        warnings.warn("GetIdentity is deprecated, use identity property instead", DeprecationWarning)
        return self.identity

    def GetCapability(self, cap):
        warnings.warn("GetCapability is deprecated, use get_capability instead", DeprecationWarning)
        return self.get_capability(cap)

    def SetCapability(self, cap, type_id, value):
        warnings.warn("SetCapability is deprecated, use set_capability instead", DeprecationWarning)
        return self.set_capability(cap, type_id, value)

    def ResetCapability(self, cap):
        warnings.warn("ResetCapability is deprecated, use reset_capability instead", DeprecationWarning)
        self.reset_capability(cap)

    def SetImageLayout(self, frame, document_number=1, page_number=1, frame_number=1):
        warnings.warn("SetImageLayout is deprecated, use set_image_layout instead", DeprecationWarning)
        self.set_image_layout(frame, document_number, page_number, frame_number)

    def GetImageLayout(self):
        warnings.warn("GetImageLayout is deprecated, use get_image_layout instead", DeprecationWarning)
        return self.get_image_layout()

    def GetDefaultImageLayout(self):
        warnings.warn("GetDefaultImageLayout is deprecated, use get_default_image_layout instead", DeprecationWarning)
        return self.get_image_layout_default()

    def ResetImageLayout(self):
        warnings.warn("ResetImageLayout is deprecated, use reset_image_layout instead", DeprecationWarning)
        self.reset_image_layout()

    def RequestAcquire(self, show_ui, modal_ui):
        warnings.warn("RequestAcquire is deprecated, use reset_acquire instead", DeprecationWarning)
        self.request_acquire(show_ui, modal_ui)

    def ModalLoop(self):
        warnings.warn("ModalLoop is deprecated, use modal_loop instead", DeprecationWarning)
        self.modal_loop()

    def HideUI(self):
        warnings.warn("HideUI is deprecated, use hide_ui instead", DeprecationWarning)
        self.hide_ui()

    def SetXferFileName(self, path, format):
        warnings.warn("SetXferFileName is deprecated, use file_xfer_params instead", DeprecationWarning)
        self.file_xfer_params = (path, format)

    def GetXferFileName(self):
        warnings.warn("GetXferFileName is deprecated, use file_xfer_params property instead", DeprecationWarning)
        return self.file_xfer_params

    def GetImageInfo(self):
        warnings.warn("GetImageInfo is deprecated, use image_info property instead", DeprecationWarning)
        return self.image_info

    def XferImageNatively(self):
        warnings.warn("XferImageNatively is deprecated, use xfer_image_natively instead", DeprecationWarning)
        return self.xfer_image_natively()

    def XferImageByFile(self):
        warnings.warn("XferImageByFile is deprecated, use xfer_image_by_file instead", DeprecationWarning)
        return self.xfer_image_by_file()


def _get_protocol_major_version(requested_protocol_major_version: None | int) -> int:
    if requested_protocol_major_version not in [None, 1, 2]:
        raise ValueError("Invalid protocol version specified")
    if utils.is_windows():
        # On Windows default to major version 1 since version 2 is not supported
        # by almost all scanners
        return 1 or requested_protocol_major_version
    else:
        return 2 or requested_protocol_major_version


def _get_dsm(dsm_name: str | None, protocol_major_version: int) -> ct.CDLL:
    if utils.is_windows():
        is64bit = sys.maxsize > 2**32
        if dsm_name:
            return ct.WinDLL(dsm_name)
        else:
            if protocol_major_version == 1 and not is64bit:
                dsm_name = os.path.join(os.environ["WINDIR"], 'twain_32.dll')
            else:
                dsm_name = "twaindsm.dll"
        try:
            logger.info("attempting to load dll: %s", dsm_name)
            return ct.WinDLL(dsm_name)
        except WindowsError as e:
            logger.error("load failed with error %s", e)
            raise excSMLoadFileFailed(e)
    else:
        return ct.CDLL('/System/Library/Frameworks/TWAIN.framework/TWAIN')


class SourceManager(object):
    """Represents a Data Source Manager connection.

    This is the first class that you need to create.

    From instance of this class you can list existing sources using :func:`source_list` property.

    You can open source using :func:`open_source` method and then use methods on
    the returned object to perform scanning.

    When done call :func:`close` method to release resources.
    """

    def __init__(self,
                 parent_window=None,
                 MajorNum: int = 1,
                 MinorNum: int = 0,
                 Language: int = TWLG_USA,
                 Country: int = TWCY_USA,
                 Info: str = "",
                 ProductName: str = "TWAIN Python Interface",
                 ProtocolMajor: int = None,
                 ProtocolMinor: int = None,
                 SupportedGroups: int = DG_IMAGE | DG_CONTROL,
                 Manufacturer: str = "pytwain",
                 ProductFamily: str = "TWAIN Python Interface",
                 dsm_name: str = None,
                 ):
        """Constructor for a TWAIN Source Manager Object. This
        constructor has one position argument, parent_window, which
        should contain .

        :param parent_window: can contain Tk, Wx or Gtk window object or the windows
            handle of the main window
        :keyword MajorNum:   default = 1
        :keyword MinorNum:   default = 0
        :keyword Language:   default = TWLG_USA
        :keyword Country:    default = TWCY_USA
        :keyword Info:       default = 'TWAIN Python Interface 1.0.0.0  10/02/2002'
        :keyword ProductName:  default = 'TWAIN Python Interface'
        :keyword ProtocolMajor: default = TWON_PROTOCOLMAJOR
        :keyword ProtocolMinor: default = TWON_PROTOCOLMINOR
        :keyword SupportedGroups: default =  DG_IMAGE | DG_CONTROL
        :keyword Manufacturer:    default =  'Kevin Gill'
        :keyword ProductFamily: default = 'TWAIN Python Interface'

        """
        self._sources = weakref.WeakSet()
        self._cb = None
        self._state = 'closed'
        self._parent_window = parent_window
        self._hwnd = 0
        if utils.is_windows():
            if hasattr(parent_window, 'winfo_id'):
                # tk window
                self._hwnd = parent_window.winfo_id()
            elif hasattr(parent_window, 'GetHandle'):
                # wx window
                self._hwnd = parent_window.GetHandle()
            elif hasattr(parent_window, 'window') and hasattr(parent_window.window, 'handle'):
                # gtk window
                self._hwnd = parent_window.window.handle
            elif parent_window is None:
                self._hwnd = 0
            else:
                self._hwnd = int(parent_window)
        protocol_major = _get_protocol_major_version(ProtocolMajor)
        twain_dll = _get_dsm(dsm_name, protocol_major_version=protocol_major)
        try:
            self._entry = twain_dll['DSM_Entry']
        except AttributeError as e:
            raise excSMGetProcAddressFailed(e)
        self._entry.restype = ct.c_uint16
        self._entry.argtypes = (ct.POINTER(TW_IDENTITY),
                                ct.POINTER(TW_IDENTITY),
                                ct.c_uint32,
                                ct.c_uint16,
                                ct.c_uint16,
                                ct.c_void_p)

        self._app_id = TW_IDENTITY(Version=TW_VERSION(MajorNum=MajorNum,
                                                      MinorNum=MinorNum,
                                                      Language=Language,
                                                      Country=Country,
                                                      Info=Info.encode('utf8')),
                                   ProtocolMajor=protocol_major,
                                   ProtocolMinor=0,
                                   SupportedGroups=SupportedGroups | DF_APP2,
                                   Manufacturer=Manufacturer.encode('utf8'),
                                   ProductFamily=ProductFamily.encode('utf8'),
                                   ProductName=ProductName.encode('utf8'))
        self._call(None, DG_CONTROL, DAT_PARENT, MSG_OPENDSM, ct.byref(ct.c_void_p(self._hwnd)))
        self._version2 = bool(self._app_id.SupportedGroups & DF_DSM2)
        if self._version2:
            entrypoint = TW_ENTRYPOINT(Size=ct.sizeof(TW_ENTRYPOINT))
            rv = self._entry(self._app_id,
                             None,
                             DG_CONTROL,
                             DAT_ENTRYPOINT,
                             MSG_GET,
                             ct.byref(entrypoint))
            if rv != TWRC_SUCCESS:
                raise excSMOpenFailed("[%s], return code %d from DG_CONTROL DAT_ENTRYPOINT MSG_GET" % (dsm_name, rv))
            self._alloc = entrypoint.DSM_MemAllocate
            self._free = entrypoint.DSM_MemFree
            self._lock = entrypoint.DSM_MemLock
            self._unlock = entrypoint.DSM_MemUnlock
            self._encode = lambda s: s.encode('utf8')
            self._decode = lambda s: s.decode('utf8')
        else:
            self._alloc = _twain1_alloc
            self._free = _twain1_free
            self._lock = _twain1_lock
            self._unlock = _twain1_unlock
            self._encoding = sys.getfilesystemencoding()
            self._encode = lambda s: s.encode(self._encoding)
            self._decode = lambda s: s.decode(self._encoding)
        logger.info("DSM initialized")
        self._state = 'open'

    def __del__(self):
        if self._state == 'open':
            self._close_dsm()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _close_dsm(self):
        self._call(None,
                   DG_CONTROL,
                   DAT_PARENT,
                   MSG_CLOSEDSM,
                   ct.byref(ct.c_void_p(self._hwnd)))

    def close(self):
        """This method is used to force the SourceManager to close down.
        It is provided for finer control than letting garbage collection drop the connections.
        """
        while self._sources:
            self._sources.pop().close()
        if self._state == 'open':
            self._close_dsm()
            self._state = 'closed'

    def _call(self, dest_id, dg: int, dat: int, msg: int, buf: typing.Any, expected_returns: tuple[int, ...] = ()) -> int:
        rv = self._entry(self._app_id, dest_id, dg, dat, msg, buf)
        if rv == TWRC_SUCCESS or rv in expected_returns:
            return rv
        elif rv == TWRC_FAILURE:
            status = TW_STATUS()
            rv = self._entry(self._app_id,
                             dest_id,
                             DG_CONTROL,
                             DAT_STATUS,
                             MSG_GET,
                             ct.byref(status))
            if rv != TWRC_SUCCESS:
                raise Exception('DG_CONTROL DAT_STATUS MSG_GET returned non success code, rv = %d' % rv)
            code = status.ConditionCode
            exc = _exc_mapping.get(code,
                                   excTWCC_UNKNOWN("ConditionCode = %d" % code))
            raise exc
        else:
            raise Exception('Unexpected result: %d' % rv)

    def _user_select(self):
        logger.info("starting source selection dialog")
        ds_id = TW_IDENTITY()
        rv = self._call(None,
                        DG_CONTROL,
                        DAT_IDENTITY,
                        MSG_USERSELECT,
                        ct.byref(ds_id),
                        (TWRC_SUCCESS, TWRC_CANCEL))
        if rv == TWRC_SUCCESS:
            logger.info("user selected source with id %s", ds_id.Id)
            return ds_id
        elif rv == TWRC_CANCEL:
            logger.info("user cancelled selection")
            return None

    def _open_ds(self, ds_id):
        logger.info("opening data source with id %s", ds_id.Id)
        self._call(None,
                   DG_CONTROL,
                   DAT_IDENTITY,
                   MSG_OPENDS,
                   ct.byref(ds_id))

    def _close_ds(self, ds_id):
        logger.info("closing data source with id %s", ds_id.Id)
        self._call(None,
                   DG_CONTROL,
                   DAT_IDENTITY,
                   MSG_CLOSEDS,
                   ct.byref(ds_id))

    def open_source(self, product_name: str = None) -> Source | None:
        """Open a TWAIN Source.

        Returns a :class:`Source` object, which can be used to communicate with the source or `None` if user cancelled
        source selection dialog.

        :keyword product_name: source to be opened, if not specified or value is `None` user will be prompted for
                               source selection
        """
        if product_name:
            ds_id = TW_IDENTITY(ProductName=self._encode(product_name))
        else:
            ds_id = self._user_select()
            if not ds_id:
                return None
        self._open_ds(ds_id)
        source = Source(self, ds_id)
        self._sources.add(source)
        return source

    @property
    def identity(self) -> dict:
        """This property is used to retrieve the identity of our application.
        The information is returned in a dictionary.
        """
        res = _struct2dict(self._app_id, self._decode)
        res.update(_struct2dict(self._app_id.Version, self._decode))
        return res

    @property
    def source_list(self) -> list[str]:
        """Returns a list containing the names of available sources"""
        names = []
        ds_id = TW_IDENTITY()
        try:
            rv = self._call(None,
                            DG_CONTROL,
                            DAT_IDENTITY,
                            MSG_GETFIRST,
                            ct.byref(ds_id),
                            (TWRC_SUCCESS, TWRC_ENDOFLIST))
        except excTWCC_NODS:
            # there are no data sources
            return names

        while rv != TWRC_ENDOFLIST:
            names.append(self._decode(ds_id.ProductName))
            rv = self._call(None,
                            DG_CONTROL,
                            DAT_IDENTITY,
                            MSG_GETNEXT,
                            ct.byref(ds_id),
                            (TWRC_SUCCESS, TWRC_ENDOFLIST))
        return names

    def set_callback(self, cb):
        """Register a python function to be used for notification that the
        transfer is ready, etc.
        """
        self._cb = cb

    def is_twain2(self) -> bool:
        return self._version2

    # backward compatible aliases
    def destroy(self):
        warnings.warn("destroy is deprecated, use close instead", DeprecationWarning)
        self.close()

    def SetCallback(self, cb):
        warnings.warn("SetCallback is deprecated, use set_callback instead", DeprecationWarning)
        return self.set_callback(cb)

    def OpenSource(self, product_name=None):
        warnings.warn("OpenSource is deprecated, use open_source instead", DeprecationWarning)
        return self.open_source(product_name)

    def GetIdentity(self):
        warnings.warn("GetIdentity is deprecated, use identity property instead", DeprecationWarning)
        return self.identity

    def GetSourceList(self):
        warnings.warn("GetSourceList is deprecated, use source_list property instead", DeprecationWarning)
        return self.source_list


def version() -> str:
    """Retrieve the version of the module"""
    return '2.0'


def acquire(path,
            ds_name=None,
            dpi=None,
            pixel_type=None,
            bpp=None,
            frame=None,
            parent_window=None,
            show_ui=False,
            dsm_name=None,
            modal=False,
            ):
    """Acquires single image into file

    :param path: Path where to save image
    :keyword ds_name: name of lowlevel data source, if not provided user will be presented with selection dialog
    :keyword dpi: resolution in dots per inch
    :keyword pixel_type: can be 'bw', 'gray', 'color'
    :keyword bpp: bits per pixel
    :keyword frame: tuple (left, top, right, bottom) scan area in inches
    :keyword parent_window: can be Tk, Wx, Gtk window object or Win32 window handle
    :keyword show_ui: if True source's UI dialog will be presented to user

    Returns a dictionary describing image, or None if scanning was cancelled by user

    """
    if pixel_type:
        pixel_type_map = {'bw': TWPT_BW,
                          'gray': TWPT_GRAY,
                          'color': TWPT_RGB}
        twain_pixel_type = pixel_type_map[pixel_type]
    if not parent_window:
        from tkinter import Tk
        parent_window = Tk()
    sm = SourceManager(parent_window, dsm_name=dsm_name)
    try:
        sd = sm.open_source(ds_name)
        if not sd:
            return None
        try:
            if pixel_type:
                sd.set_capability(ICAP_PIXELTYPE, TWTY_UINT16, twain_pixel_type)
            sd.set_capability(ICAP_UNITS, TWTY_UINT16, TWUN_INCHES)
            if bpp:
                sd.set_capability(ICAP_BITDEPTH, TWTY_UINT16, bpp)
            if dpi:
                sd.set_capability(ICAP_XRESOLUTION, TWTY_FIX32, dpi)
                sd.set_capability(ICAP_YRESOLUTION, TWTY_FIX32, dpi)
            if frame:
                try:
                    sd.set_image_layout(frame)
                except CheckStatus:
                    pass

            res = []

            def before(img_info):
                res.append(img_info)
                return path

            def after(more):
                if more:
                    raise CancelAll

            try:
                sd.acquire_file(before=before, after=after, show_ui=show_ui, modal=modal)
            except excDSTransferCancelled:
                return None
        finally:
            sd.close()
    finally:
        sm.close()
    return res[0]


# Following imports are needed for backward compatibility
from .windows import *
