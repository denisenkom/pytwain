import logging
import os
import pytest
import sys

import twain

from fixtures import root_window

logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="only for Windows")
def test_allocation(root_window):
    handle = twain.global_handle_allocate(flags=0, size=10)
    assert twain.GlobalSize(handle) == 10
    twain.GlobalLock(handle)
    twain.GlobalUnlock(handle)
    twain.global_handle_free(handle)


def test_dsm(root_window):
    with twain.SourceManager(root_window) as sm:
        if len(sm.source_list) == 0:
            pytest.skip("No Sources present on the system")
        ds_name = sm.source_list[0]
        with sm.open_source(str(ds_name)) as ds:
            val = ds.get_capability(twain.ICAP_YRESOLUTION)
            print(val)
            for v in val[1][2]:
                print(v)


def test_scan(root_window):
    logger.info("creating source manager")
    with twain.SourceManager(root_window) as sm:
        logger.info("opening source")
        with sm.open_source() as ss:  # this posts a modeless dialog...
            logger.info("request acquire")
            ss.request_acquire(show_ui=False, modal_ui=True)
            handles = []
            more = 1
            try:
                logger.info("transferring image")
                handle, more = ss.xfer_image_natively()
                handles.append(handle)
            except twain.exceptions.DSTransferCancelled:
                logger.info("cancelled")
                pass
            while more != 0:
                try:
                    logger.info("transferring image")
                    handle, more = ss.xfer_image_natively()
                    handles.append(handle)
                except twain.exceptions.DSTransferCancelled:
                    logger.info("cancelled")
                    more = 0

            logger.info("transfer complete")
            index = 0
            curr_folder = os.path.dirname(__name__)
            for handle in handles:
                twain.dib_to_bm_file(
                    handle, os.path.join(curr_folder, "testscans/{}.bmp".format(index))
                )
                twain.global_handle_free(handle)
                index += 1


def test_acquire_natively(root_window):
    """
    Testing acquire_natively method
    """
    logger.info("creating source manager")

    def save_and_close(img):
        img.save("test.bmp")
        img.close()

    with twain.SourceManager(root_window) as sm:
        logger.info("opening source")
        with sm.open_source() as ss:  # this posts a modeless dialog...
            logger.info("calling acquire_natively")
            ss.acquire_natively(after=lambda img, no: save_and_close(img))
