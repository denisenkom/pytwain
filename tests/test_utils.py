import ctypes
import ctypes as ct
from twain.windows import BITMAPINFOHEADER
from twain import exceptions
from PIL import Image


def convert_dib(ptr: ct.c_void_p):
    char_ptr = ct.cast(ptr, ct.POINTER(ct.c_char))
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
    return Image.frombuffer(mode="RGB", size=(bih.biWidth, bih.biHeight), data=(ct.c_char * dib_size).from_address(ptr.value + ctypes.sizeof(BITMAPINFOHEADER)))


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
    ptr = ct.cast((ct.c_char * 10).from_buffer(bmp_bytes, 14), ct.c_void_p)
    img2 = convert_dib(ptr)
    img_bytes = img.tobytes()
    img2_bytes = img2.tobytes()
    assert img_bytes[:100] == img2_bytes[:100]
    #img.show("original")
    #img2.show("converted")
