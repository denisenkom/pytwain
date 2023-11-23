import twain
import uuid
import logging


from fixtures import root_window


def test_multiple_images_scan(root_window):
    logging.basicConfig(level=logging.DEBUG)
    with twain.SourceManager(root_window) as sm:
        with sm.open_source() as ss:
            for _ in range(2):
                ss.request_acquire(show_ui=False, modal_ui=False)
                rv = ss.xfer_image_natively()
                if rv:
                    (handle, count) = rv
                    print(f"number of images remaining: {count}")
                    twain.dib_to_bm_file(
                        handle, "testscans/{}.bmp".format(uuid.uuid4())
                    )
                else:
                    break
                ss.hide_ui()
