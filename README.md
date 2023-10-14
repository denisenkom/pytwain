pytwain
=======
This library allows acquiring images from various sources that support TWAIN protocol, e.g. scanners.

To install this library run:
```commandline
pip install pytwain
```

Once installed you can run following sample Python script to acquire an image:
```python
import twain
import tkinter
import logging

logging.basicConfig(level=logging.DEBUG)
root = tkinter.Tk()
root.title('scan.py')
with twain.SourceManager(root) as sm:
    # this will show UI to allow user to select source
    src = sm.open_source()
    if src:
        src.request_acquire(show_ui=False, modal_ui=False)
        (handle, remaining_count) = src.xfer_image_natively()
        twain.dib_to_bm_file(handle, 'testscan.bmp')
    else:
        print("User clicked cancel")
```

Full documentation for the library located [here](http://pytwain.readthedocs.org/).

This library uses ctypes to access TWAIN API, therefore it does not require compilation and can work with Pypi.

## References
* https://twain.org/
* http://pytwain.readthedocs.org/
