from __future__ import annotations

import logging
import typing
import weakref
import warnings
import os
import sys
import ctypes as ct

from . import windows
from . import utils
from . import exceptions
from .lowlevel import constants
from .lowlevel import structs

# Following imports are needed for backward compatibility

logger = logging.getLogger("twain")

_exc_mapping = {
    constants.TWCC_BUMMER: exceptions.GeneralFailure,
    constants.TWCC_LOWMEMORY: MemoryError,
    constants.TWCC_NODS: exceptions.NoDataSourceError,
    constants.TWCC_OPERATIONERROR: exceptions.OperationError,
    constants.TWCC_BADCAP: exceptions.BadCapability,
    constants.TWCC_BADPROTOCOL: exceptions.BadProtocol,
    constants.TWCC_BADVALUE: ValueError,
    constants.TWCC_SEQERROR: exceptions.SequenceError,
    constants.TWCC_BADDEST: exceptions.BadDestination,
    constants.TWCC_CAPUNSUPPORTED: exceptions.CapUnsupported,
    constants.TWCC_CAPBADOPERATION: exceptions.CapBadOperation,
    constants.TWCC_CAPSEQERROR: exceptions.CapSeqError,
    constants.TWCC_DENIED: exceptions.DeniedError,
    constants.TWCC_FILEEXISTS: exceptions.FileExistsError,
    constants.TWCC_FILENOTFOUND: FileNotFoundError,
    constants.TWCC_NOTEMPTY: exceptions.NotEmptyError,
    constants.TWCC_PAPERJAM: exceptions.PaperJam,
    constants.TWCC_PAPERDOUBLEFEED: exceptions.PaperDoubleFeedError,
    constants.TWCC_FILEWRITEERROR: exceptions.FileWriteError,
    constants.TWCC_CHECKDEVICEONLINE: exceptions.CheckDeviceOnlineError,
    constants.TWCC_MAXCONNECTIONS: exceptions.MaxConnectionsError,
}

_ext_to_type = {
    ".bmp": constants.TWFF_BMP,
    ".jpg": constants.TWFF_JFIF,
    ".jpeg": constants.TWFF_JFIF,
    ".png": constants.TWFF_PNG,
    ".tiff": constants.TWFF_TIFF,
    ".tif": constants.TWFF_TIFF,
}

_mapping = {
    constants.TWTY_INT8: ct.c_int8,
    constants.TWTY_UINT8: ct.c_uint8,
    constants.TWTY_INT16: ct.c_int16,
    constants.TWTY_UINT16: ct.c_uint16,
    constants.TWTY_UINT32: ct.c_uint32,
    constants.TWTY_INT32: ct.c_int32,
    constants.TWTY_BOOL: ct.c_uint16,
    constants.TWTY_FIX32: structs.TW_FIX32,
    constants.TWTY_FRAME: structs.TW_FRAME,
    constants.TWTY_STR32: ct.c_char * 34,
    constants.TWTY_STR64: ct.c_char * 66,
    constants.TWTY_STR128: ct.c_char * 130,
    constants.TWTY_STR255: ct.c_char * 255,
}


def _is_good_type(type_id: int) -> bool:
    return type_id in list(_mapping.keys())


def _struct2dict(
    struct: ct.Structure, decode: typing.Callable[[bytes], str]
) -> dict[str, typing.Any]:
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


class _IImage(typing.Protocol):
    def close(self):
        ...

    def save(self, filepath: str):
        ...


if sys.platform == "win32":

    def _twain1_alloc(size: int) -> ct.c_void_p:
        return windows.GlobalAlloc(windows.GMEM_ZEROINIT, size)

    _twain1_free = windows.GlobalFree
    _twain1_lock = windows.GlobalLock
    _twain1_unlock = windows.GlobalUnlock

    class _Image(_IImage):
        def __init__(self, handle):
            self._handle = handle

        def __del__(self):
            self.close()

        def close(self):
            """Releases memory of image"""
            self._free(self._handle)  # type: ignore # needs fixing
            self._handle = None

        def save(self, filepath: str):
            """Saves in-memory image to BMP file"""
            windows.dib_write(self._handle, filepath, self._lock, self._unlock)  # type: ignore # needs fixing
else:
    # Mac
    def _twain1_alloc(size: int) -> ct.c_void_p:
        return ct.libc.malloc(size)  # type: ignore # needs fixing

    def _twain1_lock(handle):
        return handle

    def _twain1_unlock(handle):
        pass

    def _twain1_free(handle):
        return ct.libc.free(handle)


class Source:
    """
    This object represents connection to Data Source.

    An instance of this class can be created by calling
    :meth:`SourceManager.open_source`
    """

    def __init__(self, sm: SourceManager, ds_id: structs.TW_IDENTITY):
        self._sm = sm
        self._id = ds_id
        self._state = "open"
        self._version2 = bool(ds_id.SupportedGroups & constants.DF_DS2)
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
        if self._state == "ready":
            self._end_all_xfers()
        if self._state == "enabled":
            try:
                self._disable()
            except exceptions.TwainError:
                logger.warning("Failed to disable data source during cleanup")
        if self._state == "open":
            self._sm._close_ds(self._id)
            self._state = "closed"
            self._sm = None

    def _call(
        self,
        dg: int,
        dat: int,
        msg: int,
        buf,
        expected_returns=(constants.TWRC_SUCCESS,),
    ) -> int:
        return self._sm._call(self._id, dg, dat, msg, buf, expected_returns)

    def _get_capability(self, cap: int, current: int):
        twCapability = structs.TW_CAPABILITY(cap, constants.TWON_DONTCARE16, 0)
        self._call(
            constants.DG_CONTROL,
            constants.DAT_CAPABILITY,
            current,
            ct.byref(twCapability),
        )
        try:
            ptr = self._lock(twCapability.hContainer)
            try:
                if twCapability.ConType == constants.TWON_ONEVALUE:
                    type_id = int(ct.cast(ptr, ct.POINTER(ct.c_uint16))[0])
                    if not _is_good_type(type_id):
                        msg = f"Capability Code = {cap}, Format Code = {twCapability.ConType}, Item Type = {type_id}"
                        raise exceptions.CapabilityFormatNotSupported(msg)
                    ctype = _mapping.get(type_id)
                    val = ct.cast(ptr + 2, ct.POINTER(ctype))[0]  # type: ignore # needs fixing
                    if type_id in (
                        constants.TWTY_INT8,
                        constants.TWTY_UINT8,
                        constants.TWTY_INT16,
                        constants.TWTY_UINT16,
                        constants.TWTY_UINT32,
                        constants.TWTY_INT32,
                    ):
                        pass
                    elif type_id == constants.TWTY_BOOL:
                        val = bool(val)
                    elif type_id == constants.TWTY_FIX32:
                        val = structs.fix2float(val)
                    elif type_id == constants.TWTY_FRAME:
                        val = structs.frame2tuple(val)
                    return type_id, val
                elif twCapability.ConType == constants.TWON_RANGE:
                    rng = ct.cast(ptr, ct.POINTER(structs.TW_RANGE)).contents
                    return {
                        "MinValue": rng.MinValue,
                        "MaxValue": rng.MaxValue,
                        "StepSize": rng.StepSize,
                        "DefaultValue": rng.DefaultValue,
                        "CurrentValue": rng.CurrentValue,
                    }
                elif twCapability.ConType == constants.TWON_ENUMERATION:
                    enum = ct.cast(ptr, ct.POINTER(structs.TW_ENUMERATION)).contents
                    if not _is_good_type(enum.ItemType):
                        msg = f"Capability Code = {cap}, Format Code = {twCapability.ConType}, Item Type = {enum.ItemType}"
                        raise exceptions.CapabilityFormatNotSupported(msg)
                    ctype = _mapping[enum.ItemType]
                    item_p = ct.cast(
                        ptr + ct.sizeof(structs.TW_ENUMERATION), ct.POINTER(ctype)
                    )  # type: ignore # needs fixing
                    values = [el for el in item_p[0 : enum.NumItems]]
                    return enum.ItemType, (enum.CurrentIndex, enum.DefaultIndex, values)
                elif twCapability.ConType == constants.TWON_ARRAY:
                    arr = ct.cast(ptr, ct.POINTER(structs.TW_ARRAY)).contents
                    if not _is_good_type(arr.ItemType):
                        msg = f"Capability Code = {cap}, Format Code = {twCapability.ConType}, Item Type = {arr.ItemType}"
                        raise exceptions.CapabilityFormatNotSupported(msg)
                    ctype = _mapping[arr.ItemType]
                    item_p = ct.cast(
                        ptr + ct.sizeof(structs.TW_ARRAY), ct.POINTER(ctype)
                    )  # type: ignore # needs fixing
                    return arr.ItemType, [el for el in item_p[0 : arr.NumItems]]
                else:
                    msg = (
                        f"Capability Code = {cap}, Format Code = {twCapability.ConType}"
                    )
                    raise exceptions.CapabilityFormatNotSupported(msg)
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
        return self._get_capability(cap, constants.MSG_GET)

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
        return self._get_capability(cap, constants.MSG_GETCURRENT)

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
        return self._get_capability(cap, constants.MSG_GETDEFAULT)

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

    def set_capability(
        self,
        cap: int,
        type_id: int,
        value: int | float | str | tuple[float, float, float, float],
    ):
        """This function is used to set the value of a capability in the source.
        Three parameters are required, a Capability Identifier (lowlevel.CAP_* or
        lowlevel.ICAP_*) a value type (lowlevel.TWTY_*) and a value
        If the capability is not supported, an exception should be returned.
        This function is used to set a value using a TW_ONEVALUE.
        """
        if not _is_good_type(type_id):
            raise exceptions.CapabilityFormatNotSupported(
                "Capability Code = %d, Format Code = %d" % (cap, type_id)
            )
        ctype = _mapping[type_id]
        if type_id in (
            constants.TWTY_INT8,
            constants.TWTY_INT16,
            constants.TWTY_INT32,
            constants.TWTY_UINT8,
            constants.TWTY_UINT16,
            constants.TWTY_UINT32,
            constants.TWTY_BOOL,
        ):
            cval = ctype(value)  # type: ignore # needs fixing
        elif type_id in (
            constants.TWTY_STR32,
            constants.TWTY_STR64,
            constants.TWTY_STR128,
            constants.TWTY_STR255,
        ):
            cval = ctype(self._encode(value))  # type: ignore # needs fixing
        elif type_id == constants.TWTY_FIX32:
            cval = structs.float2fix(value)  # type: ignore # needs fixing
        elif type_id == constants.TWTY_FRAME:
            cval = structs.tuple2frame(value)  # type: ignore # needs fixing
        else:
            assert 0, "invalid case"
        handle = self._alloc(ct.sizeof(structs.TW_ONEVALUE) + ct.sizeof(ctype))  # type: ignore # needs fixing
        try:
            ptr = self._lock(handle)
            try:
                ct.cast(ptr, ct.POINTER(ct.c_uint16))[0] = type_id
                ct.cast(ptr + 2, ct.POINTER(ctype))[0] = cval  # type: ignore # needs fixing
            finally:
                self._unlock(handle)
            capability = structs.TW_CAPABILITY(cap, constants.TWON_ONEVALUE, handle)
            rv = self._call(
                constants.DG_CONTROL,
                constants.DAT_CAPABILITY,
                constants.MSG_SET,
                ct.byref(capability),
                [constants.TWRC_CHECKSTATUS],
            )
        finally:
            self._free(handle)
        if rv == constants.TWRC_CHECKSTATUS:
            raise exceptions.CheckStatus

    def reset_capability(self, cap: int):
        """This function is used to reset the value of a capability to the source default.

        :param cap: Capability Identifier (lowlevel.CAP_* or lowlevel.ICAP_*).
        """
        capability = structs.TW_CAPABILITY(Cap=cap)
        self._call(
            constants.DG_CONTROL,
            constants.DAT_CAPABILITY,
            constants.MSG_RESET,
            ct.byref(capability),
        )

    def set_image_layout(
        self,
        frame: tuple[float, float, float, float],
        document_number: int = 1,
        page_number: int = 1,
        frame_number: int = 1,
    ):
        """This function is used to inform the source of the Image Layout.

        It uses a tuple containing frame coordinates, document
        number, page number, frame number.
        """
        il = structs.TW_IMAGELAYOUT(
            Frame=structs.tuple2frame(frame),
            DocumentNumber=document_number,
            PageNumber=page_number,
            FrameNumber=frame_number,
        )
        rv = self._call(
            constants.DG_IMAGE,
            constants.DAT_IMAGELAYOUT,
            constants.MSG_SET,
            ct.byref(il),
            (constants.TWRC_SUCCESS, constants.TWRC_CHECKSTATUS),
        )
        if rv == constants.TWRC_CHECKSTATUS:
            raise exceptions.CheckStatus

    def get_image_layout(
        self
    ) -> tuple[tuple[float, float, float, float], int, int, int]:
        """This function is used to ask the source for Image Layout.

        It returns a tuple containing frame coordinates, document
        number, page number, frame number.

        Valid states 4 through 6
        """
        il = structs.TW_IMAGELAYOUT()
        self._call(
            constants.DG_IMAGE,
            constants.DAT_IMAGELAYOUT,
            constants.MSG_GET,
            ct.byref(il),
        )
        return (
            structs.frame2tuple(il.Frame),
            il.DocumentNumber,
            il.PageNumber,
            il.FrameNumber,
        )

    def get_image_layout_default(
        self
    ) -> tuple[tuple[float, float, float, float], int, int, int]:
        """This function is used to ask the source for default Image Layout.

        It returns a tuple containing frame coordinates, document
        number, page number, frame number.

        Valid states 4 through 6
        """
        il = structs.TW_IMAGELAYOUT()
        self._call(
            constants.DG_IMAGE,
            constants.DAT_IMAGELAYOUT,
            constants.MSG_GETDEFAULT,
            ct.byref(il),
        )
        return (
            structs.frame2tuple(il.Frame),
            il.DocumentNumber,
            il.PageNumber,
            il.FrameNumber,
        )

    def reset_image_layout(self):
        """This function is used to reset Image Layout to its default settings"""
        il = structs.TW_IMAGELAYOUT()
        self._call(
            constants.DG_IMAGE,
            constants.DAT_IMAGELAYOUT,
            constants.MSG_RESET,
            ct.byref(il),
        )

    def _enable(self, show_ui: bool, modal_ui: bool, hparent):
        """This function is used to ask the source to begin aquistion.
        Parameters:
            show_ui - bool
            modal_ui - bool
        """
        ui = structs.TW_USERINTERFACE(ShowUI=show_ui, ModalUI=modal_ui, hParent=hparent)
        logger.info("starting scan")
        self._call(
            constants.DG_CONTROL,
            constants.DAT_USERINTERFACE,
            constants.MSG_ENABLEDS,
            ct.byref(ui),
        )
        self._state = "enabled"

    def _disable(self):
        """This function is used to ask the source to hide the user interface."""
        ui = structs.TW_USERINTERFACE()
        self._call(
            constants.DG_CONTROL,
            constants.DAT_USERINTERFACE,
            constants.MSG_DISABLEDS,
            ct.byref(ui),
        )
        self._state = "open"

    def _process_event(self, msg_ref) -> tuple[int, int]:
        """The TWAIN interface requires that the windows events
        are available to both the application and the lowlevel
        source (which operates in the same process).
        This method is called in the event loop to pass on those
        events.
        """
        event = structs.TW_EVENT(ct.cast(msg_ref, ct.c_void_p), 0)
        rv = self._call(
            constants.DG_CONTROL,
            constants.DAT_EVENT,
            constants.MSG_PROCESSEVENT,
            ct.byref(event),
            (constants.TWRC_DSEVENT, constants.TWRC_NOTDSEVENT),
        )
        logger.debug("handling event result %d", rv)
        if event.TWMessage == constants.MSG_XFERREADY:
            logger.info("transfer is ready")
            self._state = "ready"
        return rv, event.TWMessage

    def _modal_loop(self, callback: typing.Callable[[int], None] | None) -> None:
        logger.info("entering modal loop")
        done = False
        msg = structs.MSG()
        while not done:
            if not windows.GetMessage(ct.byref(msg), 0, 0, 0):  # type: ignore # needs fixing
                break
            rc, event = self._process_event(ct.byref(msg))
            if rc not in (constants.TWRC_NOTDSEVENT, constants.TWRC_DSEVENT):
                logger.info("got unusual process event result %d", rc)
            if callback:
                callback(event)
            if event in (constants.MSG_XFERREADY, constants.MSG_CLOSEDSREQ):
                done = True
            if rc == constants.TWRC_NOTDSEVENT:
                windows.TranslateMessage(ct.byref(msg))  # type: ignore # needs fixing
                windows.DispatchMessage(ct.byref(msg))  # type: ignore # needs fixing
        logger.info("exited modal loop")

    def _acquire(
        self,
        callback: typing.Callable[[], int],
        show_ui: bool = True,
        modal: bool = False,
    ) -> None:
        self._enable(show_ui, modal, self._sm._hwnd)
        try:

            def callback_lolevel(event: int):
                if event == constants.MSG_XFERREADY:
                    logger.info("got MSG_XFERREADY message")
                    more = 1
                    while more:
                        try:
                            more = callback()
                        except exceptions.CancelAll:
                            self._end_all_xfers()
                            break

            self._modal_loop(callback_lolevel)
        finally:
            self._disable()

    @property
    def file_xfer_params(self) -> tuple[str, int]:
        """Property which stores tuple of (file name, format) where format is one of TWFF_*

        This property is used by :meth:`xfer_image_by_file`

        Valid states: 4, 5, 6
        """
        sfx = structs.TW_SETUPFILEXFER()
        self._call(
            constants.DG_CONTROL,
            constants.DAT_SETUPFILEXFER,
            constants.MSG_GET,
            ct.byref(sfx),
        )
        return self._decode(sfx.FileName), sfx.Format

    @file_xfer_params.setter
    def file_xfer_params(self, params: tuple[str, int]) -> None:
        (path, fmt) = params
        sfx = structs.TW_SETUPFILEXFER(self._encode(path), fmt, 0)
        self._call(
            constants.DG_CONTROL,
            constants.DAT_SETUPFILEXFER,
            constants.MSG_SET,
            ct.byref(sfx),
        )

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
        ii = structs.TW_IMAGEINFO()
        self._call(
            constants.DG_IMAGE, constants.DAT_IMAGEINFO, constants.MSG_GET, ct.byref(ii)
        )
        return {
            "XResolution": structs.fix2float(ii.XResolution),
            "YResolution": structs.fix2float(ii.YResolution),
            "ImageWidth": ii.ImageWidth,
            "ImageLength": ii.ImageLength,
            "SamplesPerPixel": ii.SamplesPerPixel,
            "BitsPerSample": list(ii.BitsPerSample),
            "BitsPerPixel": ii.BitsPerPixel,
            "Planar": ii.Planar,
            "PixelType": ii.PixelType,
            "Compression": ii.Compression,
        }

    def _get_native_image(self) -> tuple[int, ct.c_void_p]:
        hbitmap = ct.c_void_p()
        rv = self._call(
            constants.DG_IMAGE,
            constants.DAT_IMAGENATIVEXFER,
            constants.MSG_GET,
            ct.byref(hbitmap),
            (constants.TWRC_XFERDONE, constants.TWRC_CANCEL),
        )
        return rv, hbitmap

    def _get_file_image(self) -> int:
        return self._call(
            constants.DG_IMAGE,
            constants.DAT_IMAGEFILEXFER,
            constants.MSG_GET,
            None,
            (constants.TWRC_XFERDONE, constants.TWRC_CANCEL),
        )

    def _get_file_audio(self) -> int:
        return self._call(
            constants.DG_AUDIO,
            constants.DAT_AUDIOFILEXFER,
            constants.MSG_GET,
            None,
            (constants.TWRC_XFERDONE, constants.TWRC_CANCEL),
        )

    def _end_xfer(self) -> int:
        px = structs.TW_PENDINGXFERS()
        self._call(
            constants.DG_CONTROL,
            constants.DAT_PENDINGXFERS,
            constants.MSG_ENDXFER,
            ct.byref(px),
        )
        if px.Count == 0:
            self._state = "enabled"
        return px.Count

    def _end_all_xfers(self) -> None:
        """Cancel all outstanding transfers on the data source."""
        px = structs.TW_PENDINGXFERS()
        self._call(
            constants.DG_CONTROL,
            constants.DAT_PENDINGXFERS,
            constants.MSG_RESET,
            ct.byref(px),
        )
        self._state = "enabled"

    def request_acquire(self, show_ui: bool, modal_ui: bool) -> None:
        """This function is used to ask the source to begin acquisition.

        Transitions Source to state 5.

        :param show_ui: bool (default 1)
        :param modal_ui: bool (default 1)

        Valid states: 4
        """
        self._enable(show_ui, modal_ui, self._sm._hwnd)

    def modal_loop(self) -> None:
        """This function should be called after call to :func:`requiest_acquire`
        it will return after acquisition complete.

        Valid states: 5
        """
        self._modal_loop(self._sm._cb)

    def hide_ui(self) -> None:
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
        if rv == constants.TWRC_CANCEL:
            raise exceptions.DSTransferCancelled
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
        if rv == constants.TWRC_CANCEL:
            raise exceptions.DSTransferCancelled
        return more

    def acquire_file(
        self,
        before: typing.Callable[[dict], str],
        after: typing.Callable[[int], None] = lambda more: None,
        show_ui: bool = True,
        modal: bool = False,
    ) -> None:
        """Acquires one or more images as files. Call returns when acquisition complete.

        :param before: Callback called before each acquired file, it should return
                       full file path to where image should be saved. It can also throw CancelAll to cancel acquisition
        :keyword after: Callback called after each acquired file, it receives number of
                        images remaining. It can throw CancelAll to cancel remaining
                        acquisition
        :keyword show_ui: If True source's UI will be presented to user
        :keyword modal: If True source's UI will be modal
        """
        _, (_, _, mechs) = self.get_capability(constants.ICAP_XFERMECH)
        if constants.TWSX_FILE not in mechs:
            raise Exception("File transfer is not supported")

        def callback():
            filepath = before(self.image_info)
            _, ext = os.path.splitext(filepath)
            ext = ext.lower()
            if ext != ".bmp":
                import tempfile

                handle, bmppath = tempfile.mkstemp(".bmp")
                os.close(handle)
            else:
                bmppath = filepath

            self.file_xfer_params = bmppath, constants.TWFF_BMP
            rv = self._get_file_image()
            more = self._end_xfer()
            if rv == constants.TWRC_CANCEL:
                raise exceptions.DSTransferCancelled
            if ext != ".bmp":
                try:
                    import Image  # type: ignore # needs fixing
                except ImportError:
                    from PIL import Image
                Image.open(bmppath).save(filepath)
                os.remove(bmppath)
            after(more)
            return more

        self.set_capability(
            constants.ICAP_XFERMECH, constants.TWTY_UINT16, constants.TWSX_FILE
        )
        self._acquire(callback, show_ui, modal)

    def acquire_natively(
        self,
        after: typing.Callable[[_IImage, int], None],
        before: typing.Callable[[dict], None] = lambda img_info: None,
        show_ui: bool = True,
        modal: bool = False,
    ) -> None:
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
            if rv == constants.TWRC_CANCEL:
                raise exceptions.DSTransferCancelled
            after(_Image(handle), more)  # type: ignore # needs fixing
            return more

        self.set_capability(
            constants.ICAP_XFERMECH, constants.TWTY_UINT16, constants.TWSX_NATIVE
        )
        self._acquire(callback, show_ui, modal)

    def is_twain2(self) -> bool:
        return self._version2

    # backward compatible aliases
    def destroy(self) -> None:
        self.close()

    def GetCapabilityCurrent(self, cap):
        warnings.warn(
            "GetCapabilityCurrent is deprecated, use get_capability_current instead",
            DeprecationWarning,
        )
        return self.get_capability_current(cap)

    def GetCapabilityDefault(self, cap):
        warnings.warn(
            "GetCapabilityDefault is deprecated, use get_capability_default instead",
            DeprecationWarning,
        )
        return self.get_capability_default(cap)

    def GetSourceName(self):
        warnings.warn(
            "GetSourceName is deprecated, use name property instead", DeprecationWarning
        )
        return self.name

    def GetIdentity(self):
        warnings.warn(
            "GetIdentity is deprecated, use identity property instead",
            DeprecationWarning,
        )
        return self.identity

    def GetCapability(self, cap):
        warnings.warn(
            "GetCapability is deprecated, use get_capability instead",
            DeprecationWarning,
        )
        return self.get_capability(cap)

    def SetCapability(self, cap, type_id, value):
        warnings.warn(
            "SetCapability is deprecated, use set_capability instead",
            DeprecationWarning,
        )
        return self.set_capability(cap, type_id, value)

    def ResetCapability(self, cap):
        warnings.warn(
            "ResetCapability is deprecated, use reset_capability instead",
            DeprecationWarning,
        )
        self.reset_capability(cap)

    def SetImageLayout(self, frame, document_number=1, page_number=1, frame_number=1):
        warnings.warn(
            "SetImageLayout is deprecated, use set_image_layout instead",
            DeprecationWarning,
        )
        self.set_image_layout(frame, document_number, page_number, frame_number)

    def GetImageLayout(self):
        warnings.warn(
            "GetImageLayout is deprecated, use get_image_layout instead",
            DeprecationWarning,
        )
        return self.get_image_layout()

    def GetDefaultImageLayout(self):
        warnings.warn(
            "GetDefaultImageLayout is deprecated, use get_default_image_layout instead",
            DeprecationWarning,
        )
        return self.get_image_layout_default()

    def ResetImageLayout(self):
        warnings.warn(
            "ResetImageLayout is deprecated, use reset_image_layout instead",
            DeprecationWarning,
        )
        self.reset_image_layout()

    def RequestAcquire(self, show_ui, modal_ui):
        warnings.warn(
            "RequestAcquire is deprecated, use reset_acquire instead",
            DeprecationWarning,
        )
        self.request_acquire(show_ui, modal_ui)

    def ModalLoop(self):
        warnings.warn(
            "ModalLoop is deprecated, use modal_loop instead", DeprecationWarning
        )
        self.modal_loop()

    def HideUI(self):
        warnings.warn("HideUI is deprecated, use hide_ui instead", DeprecationWarning)
        self.hide_ui()

    def SetXferFileName(self, path, format):
        warnings.warn(
            "SetXferFileName is deprecated, use file_xfer_params instead",
            DeprecationWarning,
        )
        self.file_xfer_params = (path, format)

    def GetXferFileName(self):
        warnings.warn(
            "GetXferFileName is deprecated, use file_xfer_params property instead",
            DeprecationWarning,
        )
        return self.file_xfer_params

    def GetImageInfo(self):
        warnings.warn(
            "GetImageInfo is deprecated, use image_info property instead",
            DeprecationWarning,
        )
        return self.image_info

    def XferImageNatively(self):
        warnings.warn(
            "XferImageNatively is deprecated, use xfer_image_natively instead",
            DeprecationWarning,
        )
        return self.xfer_image_natively()

    def XferImageByFile(self):
        warnings.warn(
            "XferImageByFile is deprecated, use xfer_image_by_file instead",
            DeprecationWarning,
        )
        return self.xfer_image_by_file()


def _get_protocol_major_version(requested_protocol_major_version: None | int) -> int:
    if requested_protocol_major_version not in [None, 1, 2]:
        raise ValueError("Invalid protocol version specified")
    if utils.is_windows():
        # On Windows default to major version 1 since version 2 is not supported
        # by almost all scanners
        return 1 or requested_protocol_major_version
    return 2 or requested_protocol_major_version


def _get_dsm(dsm_name: str | None, protocol_major_version: int) -> ct.CDLL:
    if sys.platform == "win32":
        is64bit = sys.maxsize > 2**32
        if dsm_name:
            return ct.WinDLL(dsm_name)
        if protocol_major_version == 1 and not is64bit:
            dsm_name = os.path.join(os.environ["WINDIR"], "twain_32.dll")
        else:
            dsm_name = "twaindsm.dll"
        try:
            logger.info("attempting to load dll: %s", dsm_name)
            return ct.WinDLL(dsm_name)
        except OSError as e:
            logger.error("load failed with error %s", e)
            raise exceptions.SMLoadFileFailed(e)
    else:
        return ct.CDLL("/System/Library/Frameworks/TWAIN.framework/TWAIN")


class SourceManager:
    """Represents a Data Source Manager connection.

    This is the first class that you need to create.

    From instance of this class you can list existing sources using :func:`source_list` property.

    You can open source using :func:`open_source` method and then use methods on
    the returned object to perform scanning.

    When done call :func:`close` method to release resources.
    """

    def __init__(
        self,
        parent_window=None,
        MajorNum: int = 1,
        MinorNum: int = 0,
        Language: int = constants.TWLG_USA,
        Country: int = constants.TWCY_USA,
        Info: str = "",
        ProductName: str = "TWAIN Python Interface",
        ProtocolMajor: int | None = None,
        ProtocolMinor: int | None = None,
        SupportedGroups: int = constants.DG_IMAGE | constants.DG_CONTROL,
        Manufacturer: str = "pytwain",
        ProductFamily: str = "TWAIN Python Interface",
        dsm_name: str | None = None,
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
        self._sources: weakref.WeakSet[Source] = weakref.WeakSet()
        self._cb: typing.Callable[[int], None] | None = None
        self._state = "closed"
        self._parent_window = parent_window
        self._hwnd = 0
        if utils.is_windows():
            if hasattr(parent_window, "winfo_id"):
                # tk window
                self._hwnd = parent_window.winfo_id()
            elif hasattr(parent_window, "GetHandle"):
                # wx window
                self._hwnd = parent_window.GetHandle()
            elif hasattr(parent_window, "window") and hasattr(
                parent_window.window, "handle"
            ):
                # gtk window
                self._hwnd = parent_window.window.handle
            elif parent_window is None:
                self._hwnd = 0
            else:
                self._hwnd = int(parent_window)
        protocol_major = _get_protocol_major_version(ProtocolMajor)
        twain_dll = _get_dsm(dsm_name, protocol_major_version=protocol_major)
        try:
            self._entry = twain_dll["DSM_Entry"]
        except AttributeError as e:
            raise exceptions.SMGetProcAddressFailed(e)
        self._entry.restype = ct.c_uint16
        self._entry.argtypes = (
            ct.POINTER(structs.TW_IDENTITY),
            ct.POINTER(structs.TW_IDENTITY),
            ct.c_uint32,
            ct.c_uint16,
            ct.c_uint16,
            ct.c_void_p,
        )

        self._app_id = structs.TW_IDENTITY(
            Version=structs.TW_VERSION(
                MajorNum=MajorNum,
                MinorNum=MinorNum,
                Language=Language,
                Country=Country,
                Info=Info.encode("utf8"),
            ),
            ProtocolMajor=protocol_major,
            ProtocolMinor=0,
            SupportedGroups=SupportedGroups | constants.DF_APP2,
            Manufacturer=Manufacturer.encode("utf8"),
            ProductFamily=ProductFamily.encode("utf8"),
            ProductName=ProductName.encode("utf8"),
        )
        self._call(
            None,
            constants.DG_CONTROL,
            constants.DAT_PARENT,
            constants.MSG_OPENDSM,
            ct.byref(ct.c_void_p(self._hwnd)),
        )
        self._version2 = bool(self._app_id.SupportedGroups & constants.DF_DSM2)
        if self._version2:
            entrypoint = structs.TW_ENTRYPOINT(Size=ct.sizeof(structs.TW_ENTRYPOINT))
            rv = self._entry(
                self._app_id,
                None,
                constants.DG_CONTROL,
                constants.DAT_ENTRYPOINT,
                constants.MSG_GET,
                ct.byref(entrypoint),
            )
            if rv != constants.TWRC_SUCCESS:
                raise exceptions.SMOpenFailed(
                    "[%s], return code %d from DG_CONTROL DAT_ENTRYPOINT MSG_GET"
                    % (dsm_name, rv)
                )
            self._alloc = entrypoint.DSM_MemAllocate
            self._free = entrypoint.DSM_MemFree
            self._lock = entrypoint.DSM_MemLock
            self._unlock = entrypoint.DSM_MemUnlock
            self._encode = lambda s: s.encode("utf8")
            self._decode = lambda s: s.decode("utf8")
        else:
            self._alloc = _twain1_alloc
            self._free = _twain1_free
            self._lock = _twain1_lock
            self._unlock = _twain1_unlock
            self._encoding = sys.getfilesystemencoding()
            self._encode = lambda s: s.encode(self._encoding)
            self._decode = lambda s: s.decode(self._encoding)
        logger.info("DSM initialized")
        self._state = "open"

    def __del__(self) -> None:
        if self._state == "open":
            self._close_dsm()

    def __enter__(self) -> SourceManager:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def _close_dsm(self) -> None:
        self._call(
            None,
            constants.DG_CONTROL,
            constants.DAT_PARENT,
            constants.MSG_CLOSEDSM,
            ct.byref(ct.c_void_p(self._hwnd)),
        )

    def close(self) -> None:
        """This method is used to force the SourceManager to close down.
        It is provided for finer control than letting garbage collection drop the connections.
        """
        while self._sources:
            self._sources.pop().close()
        if self._state == "open":
            self._close_dsm()
            self._state = "closed"

    def _call(
        self,
        dest_id,
        dg: int,
        dat: int,
        msg: int,
        buf: typing.Any,
        expected_returns: tuple[int, ...] = (),
    ) -> int:
        rv = self._entry(self._app_id, dest_id, dg, dat, msg, buf)
        if rv == constants.TWRC_SUCCESS or rv in expected_returns:
            return rv
        elif rv == constants.TWRC_FAILURE:
            status = structs.TW_STATUS()
            rv = self._entry(
                self._app_id,
                dest_id,
                constants.DG_CONTROL,
                constants.DAT_STATUS,
                constants.MSG_GET,
                ct.byref(status),
            )
            if rv != constants.TWRC_SUCCESS:
                logger.warning(
                    f"Getting additional error information returned non success code: {rv}"
                )
                raise exceptions.TwainError()
            code = status.ConditionCode
            exc = _exc_mapping.get(
                code, exceptions.UnknownError("ConditionCode = %d" % code)
            )
            raise exc
        else:
            raise RuntimeError("Unexpected result: %d" % rv)

    def _user_select(self) -> structs.TW_IDENTITY | None:
        logger.info("starting source selection dialog")
        ds_id = structs.TW_IDENTITY()
        rv = self._call(
            None,
            constants.DG_CONTROL,
            constants.DAT_IDENTITY,
            constants.MSG_USERSELECT,
            ct.byref(ds_id),
            expected_returns=(constants.TWRC_SUCCESS, constants.TWRC_CANCEL),
        )
        if rv == constants.TWRC_SUCCESS:
            logger.info("user selected source with id %s", ds_id.Id)
            return ds_id
        elif rv == constants.TWRC_CANCEL:
            logger.info("user cancelled selection")
            return None
        else:
            # This is unexpected since _call should only return values from expected_returns list
            raise RuntimeError(f"Got unexpected return value {rv} from _call method")

    def _open_ds(self, ds_id: structs.TW_IDENTITY) -> None:
        logger.info("opening data source with id %s", ds_id.Id)
        self._call(
            None,
            constants.DG_CONTROL,
            constants.DAT_IDENTITY,
            constants.MSG_OPENDS,
            ct.byref(ds_id),
        )

    def _close_ds(self, ds_id: structs.TW_IDENTITY) -> None:
        logger.info("closing data source with id %s", ds_id.Id)
        self._call(
            None,
            constants.DG_CONTROL,
            constants.DAT_IDENTITY,
            constants.MSG_CLOSEDS,
            ct.byref(ds_id),
        )

    def open_source(self, product_name: str | None = None) -> Source | None:
        """Open a TWAIN Source.

        If `product_name` parameter is specified, will open source matching that product name.
        Otherwise, will present a source selection dialog box to user.  Once user selects a source,
        that source will be opened.

        Returns a :class:`Source` object, which can be used to communicate with the source or `None` if user cancelled
        source selection dialog.

        :keyword product_name: source to be opened, if not specified or value is `None` user will be prompted for
                               source selection
        """
        if product_name:
            ds_id = structs.TW_IDENTITY(ProductName=self._encode(product_name))
        else:
            selected_ds_id = self._user_select()
            if not selected_ds_id:
                return None
            ds_id = selected_ds_id
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
        names: typing.List[str] = []
        ds_id = structs.TW_IDENTITY()
        try:
            rv = self._call(
                None,
                constants.DG_CONTROL,
                constants.DAT_IDENTITY,
                constants.MSG_GETFIRST,
                ct.byref(ds_id),
                (constants.TWRC_SUCCESS, constants.TWRC_ENDOFLIST),
            )
        except exceptions.NoDataSourceError:
            # there are no data sources
            return names

        while rv != constants.TWRC_ENDOFLIST:
            names.append(self._decode(ds_id.ProductName))
            rv = self._call(
                None,
                constants.DG_CONTROL,
                constants.DAT_IDENTITY,
                constants.MSG_GETNEXT,
                ct.byref(ds_id),
                (constants.TWRC_SUCCESS, constants.TWRC_ENDOFLIST),
            )
        return names

    def set_callback(self, cb: typing.Callable[[int], None] | None):
        """Register a python function to be used for notification that the
        transfer is ready, etc.
        """
        self._cb = cb

    def is_twain2(self) -> bool:
        return self._version2

    # backward compatible aliases
    def destroy(self) -> None:
        warnings.warn("destroy is deprecated, use close instead", DeprecationWarning)
        self.close()

    def SetCallback(self, cb):
        warnings.warn(
            "SetCallback is deprecated, use set_callback instead", DeprecationWarning
        )
        return self.set_callback(cb)

    def OpenSource(self, product_name=None):
        warnings.warn(
            "OpenSource is deprecated, use open_source instead", DeprecationWarning
        )
        return self.open_source(product_name)

    def GetIdentity(self):
        warnings.warn(
            "GetIdentity is deprecated, use identity property instead",
            DeprecationWarning,
        )
        return self.identity

    def GetSourceList(self):
        warnings.warn(
            "GetSourceList is deprecated, use source_list property instead",
            DeprecationWarning,
        )
        return self.source_list


def version() -> str:
    """Retrieve the version of the module"""
    # This version should be updated before release.
    # Ideally it needs to be automated with build process.
    return "2.2.1"


def acquire(
    path: str,
    ds_name: str | None = None,
    dpi: float | None = None,
    pixel_type: typing.Literal["bw", "gray", "color"] | None = None,
    bpp: int | None = None,
    frame: tuple[float, float, float, float] | None = None,
    parent_window=None,
    show_ui: bool = False,
    dsm_name: str | None = None,
    modal: bool = False,
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
        pixel_type_map = {
            "bw": constants.TWPT_BW,
            "gray": constants.TWPT_GRAY,
            "color": constants.TWPT_RGB,
        }
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
                sd.set_capability(
                    constants.ICAP_PIXELTYPE, constants.TWTY_UINT16, twain_pixel_type
                )
            sd.set_capability(
                constants.ICAP_UNITS, constants.TWTY_UINT16, constants.TWUN_INCHES
            )
            if bpp:
                sd.set_capability(constants.ICAP_BITDEPTH, constants.TWTY_UINT16, bpp)
            if dpi:
                sd.set_capability(constants.ICAP_XRESOLUTION, constants.TWTY_FIX32, dpi)
                sd.set_capability(constants.ICAP_YRESOLUTION, constants.TWTY_FIX32, dpi)
            if frame:
                try:
                    sd.set_image_layout(frame)
                except exceptions.CheckStatus:
                    pass

            res = []

            def before(img_info):
                res.append(img_info)
                return path

            def after(more):
                if more:
                    raise exceptions.CancelAll

            try:
                sd.acquire_file(
                    before=before, after=after, show_ui=show_ui, modal=modal
                )
            except exceptions.DSTransferCancelled:
                return None
        finally:
            sd.close()
    finally:
        sm.close()
    return res[0]
