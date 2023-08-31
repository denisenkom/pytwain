import ctypes as ct
import warnings
from . import exceptions


def _win_check(result, func, args):
    if func is GlobalFree:
        if result:
            raise ct.WinError()
        return None
    elif func is GlobalUnlock:
        if not result and ct.GetLastError() != 0:
            raise ct.WinError()
        return result
    elif func is GetMessage:
        if result == -1:
            raise ct.WinError()
        return result
    elif func is TranslateMessage or func is DispatchMessage:
        return result
    else:
        if not result:
            raise ct.WinError()
        return result


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


class BITMAPINFOHEADER(ct.Structure):
    _pack_ = 4
    _fields_ = [('biSize', ct.c_uint32),
                ('biWidth', ct.c_long),
                ('biHeight', ct.c_long),
                ('biPlanes', ct.c_uint16),
                ('biBitCount', ct.c_uint16),
                ('biCompression', ct.c_uint32),
                ('biSizeImage', ct.c_uint32),
                ('biXPelsPerMeter', ct.c_long),
                ('biYPelsPerMeter', ct.c_long),
                ('biClrUsed', ct.c_uint32),
                ('biClrImportant', ct.c_uint32)]


def _dib_write(handle, path, lock, unlock):
    file_header_size = 14
    ptr = lock(handle)
    try:
        char_ptr = ct.cast(ptr, ct.POINTER(ct.c_char))
        bih = ct.cast(ptr, ct.POINTER(BITMAPINFOHEADER)).contents
        if bih.biCompression != 0:
            msg = 'Cannot handle compressed image. Compression Format %d' % bih.biCompression
            raise exceptions.excImageFormat(msg)
        bits_offset = file_header_size + bih.biSize + bih.biClrUsed * 4
        if bih.biSizeImage == 0:
            row_bytes = (((bih.biWidth * bih.biBitCount) + 31) & ~31) // 8
            bih.biSizeImage = row_bytes * bih.biHeight
        dib_size = bih.biSize + bih.biClrUsed * 4 + bih.biSizeImage
        file_size = dib_size + file_header_size

        def _write_bmp(f):
            import struct
            f.write(b'BM')
            f.write(struct.pack('LHHL', file_size, 0, 0, bits_offset))
            for i in range(dib_size):
                f.write(char_ptr[i])

        if path:
            f = open(path, 'wb')
            try:
                _write_bmp(f)
            finally:
                f.close()
        else:
            import io
            f = io.BytesIO()
            try:
                _write_bmp(f)
                return f.getvalue()
            finally:
                f.close()
    finally:
        unlock(handle)


def dib_to_bm_file(handle, path=None):
    """Convert a DIB (Device Independent Bitmap) to a windows
    bitmap file format. The BitMap file is either returned as
    a string, or written to a file with the name given in the
    second argument.

    .. note::

        Can only be used with lowlevel 1.x sources
    """
    return _dib_write(handle, path, GlobalLock, GlobalUnlock)


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
    import tempfile
    import os
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
