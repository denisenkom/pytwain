import twain.utils

from PIL import Image


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
    img2 = twain.utils.convert_dib_to_bmp(bmp_bytes[hdr_size:])
    assert bmp_bytes[:100] == img2[:100]
