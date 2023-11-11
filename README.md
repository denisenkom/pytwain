pytwain
=======
This library allows acquiring images from various sources that support TWAIN protocol, e.g. scanners.

To install this library run:
```commandline
pip install pytwain
```

Once installed you can run following sample Python script to acquire an image:
```python
from io import BytesIO
import twain
import tkinter
from tkinter import ttk
import logging
import PIL.ImageTk
import PIL.Image

scanned_image = None


def scan():
    global scanned_image
    with twain.SourceManager(root) as sm:
        # this will show UI to allow user to select source
        src = sm.open_source()
        if src:
            src.request_acquire(show_ui=False, modal_ui=False)
            (handle, remaining_count) = src.xfer_image_natively()
            bmp_bytes = twain.dib_to_bm_file(handle)
            img = PIL.Image.open(BytesIO(bmp_bytes), formats=["bmp"])
            width, height = img.size
            factor = 600.0 / width
            # Storing PhotoImage in global variable to prevent it from being deleted once this function exits
            # since PhotoImage has a __del__ destructor
            scanned_image = PIL.ImageTk.PhotoImage(img.resize(size=(int(width * factor), int(height * factor))))
            frm.destroy()
            ttk.Label(root, image=scanned_image).pack(side="left", fill="both", expand=1)
        else:
            print("User clicked cancel")


logging.basicConfig(level=logging.DEBUG)
root = tkinter.Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Button(frm, text="Scan", command=scan).grid(column=0, row=0)
root.mainloop()
```

Full documentation for the library located [here](http://pytwain.readthedocs.org/).

This library uses ctypes to access TWAIN API, therefore it does not require compilation and can work with Pypi.

## References
* https://twain.org/
* http://pytwain.readthedocs.org/
