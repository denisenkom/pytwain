import unittest
import logging
import os

import tkinter

import twain

logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)


class MyTestCase(unittest.TestCase):
    def test_allocation(self):
        handle = twain.global_handle_allocate(flags=0, size=10)
        assert twain.GlobalSize(handle) == 10
        twain.GlobalLock(handle)
        twain.GlobalUnlock(handle)
        twain.global_handle_free(handle)

    def test_dsm(self):
        import twain
        root = tkinter.Tk()
        root.title('scan.py')
        with twain.SourceManager(root) as sm:
            if len(sm.source_list) == 0:
                self.skipTest('No Sources present on the system')
            ds_name = sm.source_list[0]
            with sm.open_source(str(ds_name)) as ds:
                val = ds.get_capability(twain.ICAP_YRESOLUTION)
                print(val)
                for v in val[1][2]:
                    print(v)

    def test_scan(self):
        import twain
        root = tkinter.Tk()
        root.title('scan.py')
        logger.info('creating source manager')
        with twain.SourceManager(root) as sm:
            logger.info('opening source')
            with sm.open_source() as ss:  # this posts a modeless dialog...
                logger.info('request acquire')
                ss.request_acquire(show_ui=False, modal_ui=True)
                handles = []
                more = 1
                try:
                    logger.info('transferring image')
                    handle, more = ss.xfer_image_natively()
                    handles.append(handle)
                except twain.exceptions.DSTransferCancelled:
                    logger.info('cancelled')
                    pass
                while more != 0:
                    try:
                        logger.info('transferring image')
                        handle, more = ss.xfer_image_natively()
                        handles.append(handle)
                    except twain.exceptions.DSTransferCancelled:
                        logger.info('cancelled')
                        more = 0

                logger.info('transfer complete')
                index = 0
                curr_folder = os.path.dirname(__name__)
                for handle in handles:
                    twain.dib_to_bm_file(handle, os.path.join(curr_folder, "testscans/{}.bmp".format(index)))
                    twain.global_handle_free(handle)
                    index += 1