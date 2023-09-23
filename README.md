pytwain
=======
This is a native Python library for TWAIN API.

To install this library run:
```commandline
pip install pytwain
```

Once installed you can run following sample Python script to scan one image:
```python
import twain
import tkinter
import logging

logging.basicConfig(level=logging.DEBUG)
root = tkinter.Tk()
root.title('scan.py')
sm = twain.SourceManager(root)
src = sm.open_source()
src.request_acquire(show_ui=False, modal_ui=False)
(handle, remaining_count) = src.xfer_image_natively()
twain.dib_to_bm_file(handle, 'testscan.bmp')
```

Full documentation for the library located [here](http://pytwain.readthedocs.org/).

## References
* https://twain.org/
* http://pytwain.readthedocs.org/
