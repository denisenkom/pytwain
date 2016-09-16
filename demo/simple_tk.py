"""simple_tk.py

This is a simple demonstration of the twain module using Tkinter.

This version does not use callbacks. Instead, it polls to check to
see if the image is ready. Callbacks do not work with twainmodule and
Tkinter in python 2.5
"""

from tkinter import *

from simple_base import TwainBase

import traceback, sys

TITLE="Simple Twain Demo Using Tkinter"

class MainWindow(Frame, TwainBase):
    def __init__(self, title):
        Frame.__init__(self, colormap="new", visual="truecolor")
        self.master.title(title)
        self.master.geometry("500x500+100+100")
        MenuPanel = Frame(self, relief=RAISED, borderwidth=2)
        File = Menubutton(MenuPanel, text="File")
        File.menu = Menu(File)
        File.menu.add_command(label="Connect", command=self.MnuOpenScanner)
        File.menu.add_command(label="Acquire Natively", command=self.MnuAcquireNatively)
        File.menu.add_command(label="Acquire By File", command=self.MnuAcquireByFile)
        File.menu.add('separator')
        File.menu.add_command(label="Exit", command=self.MnuQuit)
        File['menu'] = File.menu
        File.pack(side="left")
        MenuPanel.pack(side="top", fill=X, expand=1)
        self.tk_menuBar(File)
        self.pack(fill="both")
        self.bind('<Destroy>', self.OnQuit)

        self.imageLabel = Label(self)
        self.imageLabel.pack(side="left", fill="both", expand=1)

        # Print out the exception - requires that you run from the command prompt
        sys.excepthook = traceback.print_exception

        # Initialise TWAIN Base class
        self.Initialise()

        # Initialise Idle Timer
        self.after(250, self.OnIdleTimer)

    def MnuQuit(self, event=None):
        self.unbind('<Destroy>')
        self.Terminate()          # Terminate base class
        self.quit()

    def OnQuit(self, event=None):
        self.Terminate()

    def MnuOpenScanner(self, event=None):
        self.OpenScanner(self.winfo_id(), ProductName="Simple Tk Demo")

    def MnuAcquireNatively(self, event=None):
        self.AcquireNatively()

    def MnuAcquireByFile(self, event=None):
        self.AcquireByFile()

    def DisplayImage(self, filename):
        try:
            import ImageTk  # PIL required
        except ImportError:
            from PIL import ImageTk
        try:
            imagedata = ImageTk.PhotoImage(file=filename)
            self.imageLabel.config(image=imagedata)
            self.imageLabel.pack(side="left", fill="both", expand=1)
            self.master.title(filename)
            # Need to keep this object resident
            self.imagedata= imagedata
        except:
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2])
            
    def LogMessage(self, message):
        self.master.title(message)

    def OnIdleTimer(self):
        self.PollForImage()
        self.after(250, self.OnIdleTimer)

MainWindow(TITLE).mainloop()
 
