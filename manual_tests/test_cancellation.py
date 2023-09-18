import twain
import logging
import tkinter


def print_green(str):
    print(f"\033[92m{str}\033[00m")


logging.basicConfig(level=logging.DEBUG)
root = tkinter.Tk()
root.title('testing cancellation')
sm = twain.SourceManager(root)
ss = sm.open_source()
ss.request_acquire(show_ui=False, modal_ui=False)
try:
    rv = ss.xfer_image_natively()
except twain.exceptions.DSTransferCancelled:
    print_green("SUCCESS")
else:
    raise RuntimeError("Cancellation exception was not raised, did you forget to cancel transfer?")