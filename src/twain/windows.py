import ctypes as ct
import tempfile
import os
import warnings
from . import utils
from .utils import convert_dib_to_bmp


def _win_check(result, func, _):
    if func is GlobalFree:
        if result:
            raise ct.WinError()
        return None
    if func is GlobalUnlock:
        if not result and ct.GetLastError() != 0:
            raise ct.WinError()
        return result
    if func is GetMessage:
        if result == -1:
            raise ct.WinError()
        return result
    if func is TranslateMessage or func is DispatchMessage:
        return result
    if not result:
        raise ct.WinError()
    return result


if utils.is_windows():
    GlobalLock = ct.windll.kernel32.GlobalLock
    GlobalLock.argtypes = [ct.c_void_p]
    GlobalLock.restype = ct.c_void_p
    GlobalLock.errcheck = _win_check
    GlobalUnlock = ct.windll.kernel32.GlobalUnlock
    GlobalUnlock.argtypes = [ct.c_void_p]
    GlobalUnlock.errcheck = _win_check
    GlobalAlloc = ct.windll.kernel32.GlobalAlloc
    GlobalAlloc.restype = ct.c_void_p
    GlobalAlloc.errcheck = _win_check
    GlobalFree = ct.windll.kernel32.GlobalFree
    GlobalFree.argtypes = [ct.c_void_p]
    GlobalFree.errcheck = _win_check
    GlobalSize = ct.windll.kernel32.GlobalSize
    GlobalSize.argtypes = [ct.c_void_p]
    GlobalSize.restype = ct.c_size_t
    GlobalSize.errcheck = _win_check
    GetMessage = ct.windll.user32.GetMessageW
    TranslateMessage = ct.windll.user32.TranslateMessage
    TranslateMessage.errcheck = _win_check
    DispatchMessage = ct.windll.user32.DispatchMessageW
    DispatchMessage.errcheck = _win_check

GMEM_ZEROINIT = 0x0040


def dib_to_bm_file(handle, path=None):
    """Convert a DIB (Device Independent Bitmap) to a windows
    bitmap file format. The BitMap file is either returned as
    a string, or written to a file with the name given in the
    second argument.

    .. note::

        Can only be used with lowlevel 1.x sources
    """
    size = GlobalSize(handle)
    ptr = GlobalLock(handle)
    try:
        dib_bytes = (ct.c_char * size).from_address(ptr)
        bmp = convert_dib_to_bmp(dib_bytes)
        if path:
            with open(path, 'wb') as f:
                f.write(bmp)
        else:
            return bmp
    finally:
        GlobalUnlock(handle)
    return None


def dib_to_xbm_file(handle, path=None):
    """Convert a DIB (Device Independent Bitmap) to an X-Windows
    bitmap file (XBM format). The XBM file is either returned as
    a string, or written to a file with the name given in the
    third argument.
    Parameters:

    :param handle: Handle to a global area containing a DIB,
    :param path: Path prefix to be used for the name and an optional filename
        for file only output.

    .. note::

        Can only be used with lowlevel 1.x sources
    """
    handle, bmppath = tempfile.mkstemp('.bmp')
    os.close(handle)
    dib_to_bm_file(handle, bmppath)
    try:
        import Image
    except ImportError:
        from PIL import Image
    Image.open(bmppath).save(path, 'xbm')
    os.remove(bmppath)


def global_handle_get_bytes(handle, offset, count):
    """Read a specified number of bytes from a global handle.

    Parameters:
    :param handle: Global handle
    :param offset: An index into the handle data
    :param count: The number of bytes to be returned

    .. note::

        Can only be used with lowlevel 1.x sources
    """
    size = GlobalSize(handle)
    ptr = GlobalLock(handle)
    try:
        char_ptr = ct.cast(ptr, ct.POINTER(ct.c_char))
        return char_ptr[min(offset, size) : min(offset + count, size)]
    finally:
        GlobalUnlock(handle)


def global_handle_put_bytes(handle, offset, count, data):
    """Write a specified number of bytes to a global handle.

    Parameters:

    :param handle: Global handle
    :param offset: An index into the handle data
    :param count: The number of bytes to update
    :param data: String of data to be written

    .. note::

        Can only be used with lowlevel 1.x sources
    """
    size = GlobalSize(handle)
    ptr = GlobalLock(handle)
    try:
        char_ptr = ct.cast(ptr, ct.POINTER(ct.c_char))
        offset = min(offset, size)
        end = min(offset + count, size)
        count = end - offset
        count = min(count, len(data))
        for i in range(count):
            char_ptr[i + offset] = data[i]
    finally:
        GlobalUnlock(handle)


def global_handle_allocate(flags, size):
    """Allocate a specified number of bytes via a global handle.

    Parameters:

    :param size: The number of bytes to be allocated

    .. note::

        Can only be used with lowlevel 1.x sources
    """
    return GlobalAlloc(flags, size)


def global_handle_free(handle):
    """Free an allocated heap section via the global handle.

    Parameters:

    :param handle: Handle to memory to be freed

    .. note::

        Can only be used with lowlevel 1.x sources
    """
    return GlobalFree(handle)


# backward compatible aliases
def DIBToBMFile(handle, path=None):
    """ Backward compatible alias for :func:`dib_to_bm_file` """
    warnings.warn("DIBToBMFile is deprecated, use dib_to_bm_file instead", DeprecationWarning)
    return dib_to_bm_file(handle, path)


def DIBToXBMFile(handle, path=None):
    """ Backward compatible alias for :func:`dib_to_xbm_file` """
    warnings.warn("DIBToXBMFile is deprecated, use dib_to_xbm_file instead", DeprecationWarning)
    return dib_to_xbm_file(handle, path)


def GlobalHandleGetBytes(handle, offset, count):
    """ Backward compatible alias for :func:`global_handle_get_bytes` """
    warnings.warn("GlobalHandleGetBytes is deprecated, use global_handle_get_bytes instead", DeprecationWarning)
    return global_handle_get_bytes(handle, offset, count)


def GlobalHandlePutBytes(handle, offset, count, data):
    """ Backward compatible alias for :func:`global_handle_put_bytes` """
    warnings.warn("GlobalHandlePutBytes is deprecated, use global_handle_put_bytes instead", DeprecationWarning)
    return global_handle_put_bytes(handle, offset, count, data)


def GlobalHandleAllocate(flags, size):
    """ Backward compatible alias for :func:`global_handle_allocate` """
    warnings.warn("GlobalHandleAllocate is deprecated, use global_handle_allocate instead", DeprecationWarning)
    return global_handle_allocate(flags, size)


def GlobalHandleFree(handle):
    """ Backward compatible alias for :func:`global_handle_free` """
    warnings.warn("GlobalHandleFree is deprecated, use global_handle_free instead", DeprecationWarning)
    return global_handle_free(handle)
