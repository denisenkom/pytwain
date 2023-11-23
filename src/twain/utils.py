from __future__ import annotations

import platform
import ctypes as ct
import struct


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


def is_windows() -> bool:
    """
    Returns true if running on Windows
    """
    return platform.system() == 'Windows'


def convert_dib_to_bmp(dib_bytes: bytes | ct.Array[ct.c_char]) -> bytes:
    """
    Convert image from Device Independent Bitmap (DIB) passed as bytes array
    to BMP file format.  Since BMP file format is just a DIB with BMP file header,
    this function just prepends DIB with said header.

    DIB is the image format used by TWAIN on Windows.
    More information on DIB format can be found here: https://learn.microsoft.com/en-us/windows/win32/gdi/device-independent-bitmaps
    """
    file_header_size = 14
    bih = BITMAPINFOHEADER.from_buffer(dib_bytes)
    bits_offset = file_header_size + bih.biSize + bih.biClrUsed * 4
    file_size = len(dib_bytes) + file_header_size
    file_header = struct.pack('=ccLHHL', b"B", b"M", file_size, 0, 0, bits_offset)
    return file_header + dib_bytes
