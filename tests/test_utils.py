import ctypes
import ctypes as ct
from io import BytesIO

from twain.windows import BITMAPINFOHEADER
from twain import exceptions
from PIL import Image


def convert_dib(ptr: ct.c_void_p):
    """
    Manual conversion
    """
    bih = ct.cast(ptr, ct.POINTER(BITMAPINFOHEADER)).contents
    if bih.biCompression != 0:
        msg = 'Cannot handle compressed image. Compression Format %d' % bih.biCompression
        raise exceptions.ImageFormatNotSupported(msg)
    #bits_offset = file_header_size + bih.biSize + bih.biClrUsed * 4
    if bih.biSizeImage == 0:
        row_bytes = (((bih.biWidth * bih.biBitCount) + 31) & ~31) // 8
        bih.biSizeImage = row_bytes * bih.biHeight
    dib_size = bih.biSize + bih.biClrUsed * 4 + bih.biSizeImage
    #file_size = dib_size + file_header_size
    # TODO: mode should be properly determined from header
    img = Image.frombuffer(mode="RGBA", size=(bih.biWidth, bih.biHeight), data=(ct.c_char * dib_size).from_address(ptr.value + ctypes.sizeof(BITMAPINFOHEADER)))
    r, g, b, a = img.split()
    return Image.merge("RGB", (b, g, r)).transpose(Image.FLIP_TOP_BOTTOM)


def convert_dib2(dib: bytes, orig_header: bytes):
    file_header_size = 14
    file_size = file_header_size + len(dib)
    bih = BITMAPINFOHEADER.from_buffer(dib)
    bits_offset = file_header_size + bih.biSize + bih.biClrUsed * 4
    import struct
    file_header = struct.pack('=ccLHHL', b"B", b"M", file_size, 0, 0, bits_offset)
    return Image.open(BytesIO(file_header + dib), formats=["bmp"])


def test_bitmap_conversion():
    """
    Test device independent bitmap in-memory conversion
    """
    # Create test image
    test_image_path = "SMPTE_Color_Bars.bmp"
    img = Image.open(test_image_path)
    print(img.mode)
    # Load it as raw bytes
    with open(test_image_path, "rb") as fp:
        bmp_bytes = bytearray(fp.read())
    # skipping first 14 bytes of file header to get to BITMAPINFOHEADER structure
    hdr_size = 14
    ptr = ct.cast((ct.c_char * (len(bmp_bytes) - hdr_size)).from_buffer(bmp_bytes, hdr_size), ct.c_void_p)
    img2 = convert_dib2(bmp_bytes[hdr_size:], bmp_bytes[:hdr_size])
    img_bytes = img.tobytes()
    img2_bytes = img2.tobytes()
    #assert img_bytes[:100] == img2_bytes[:100]
    img.show("original")
    img2.show("converted")
