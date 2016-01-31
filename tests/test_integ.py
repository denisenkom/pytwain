import unittest


class MyTestCase(unittest.TestCase):
    def test_dsm(self):
        import twain
        sm = twain.SourceManager()
        print(sm.source_list)
