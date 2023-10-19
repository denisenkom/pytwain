import platform
import ctypes as ct


class BITMAPINFOHEADER(ct.Structure):
    _pack_ = 4
    _fields_ = [('biSize', ct.c_uint32),
                ('biWidth', ct.c_int32),
                ('biHeight', ct.c_int32),
                ('biPlanes', ct.c_uint16),
                ('biBitCount', ct.c_uint16),
                ('biCompression', ct.c_uint32),
                ('biSizeImage', ct.c_uint32),
                ('biXPelsPerMeter', ct.c_int32),
                ('biYPelsPerMeter', ct.c_int32),
                ('biClrUsed', ct.c_uint32),
                ('biClrImportant', ct.c_uint32)]


def is_windows():
    """
    Returns true if running on Windows
    """
    return platform.system() == 'Windows'


def convert_dib_to_bmp(dib_ptr: ct.c_void_p) -> bytes:
    file_header_size = 14
    bih = ct.cast(dib_ptr, ct.POINTER(BITMAPINFOHEADER)).contents
    bits_offset = file_header_size + bih.biSize + bih.biClrUsed * 4
    dib_size = bih.biSize + bih.biClrUsed * 4 + bih.biSizeImage
    file_size = dib_size + file_header_size
    import struct
    file_header = struct.pack('=ccLHHL', b"B", b"M", file_size, 0, 0, bits_offset)
    return file_header + ct.cast(dib_ptr, ct.c_char * dib_size)
