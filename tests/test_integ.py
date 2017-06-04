import unittest
from six.moves import tkinter


class MyTestCase(unittest.TestCase):
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
