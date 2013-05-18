"""simple_wx3.py

Demonstration of the twain module using the wxPython windows toolkit.

This version does uses callbacks. Polling can be used instead by
modifying the global variable USE_CALLBACK below.
"""

import wx

from simple_base import TwainBase

import traceback, sys

ID_EXIT=102
ID_OPEN_SCANNER=103
ID_ACQUIRE_NATIVELY=104
ID_SCROLLEDWINDOW1=105
ID_BMPIMAGE=106
ID_ACQUIRE_BY_FILE=107
ID_TIMER=108

# You can either Poll the TWAIN source, or process the scanned image in an
# event callback. The event callback has not been fully tested using GTK.
# Specifically this does not work with Tkinter.
USE_CALLBACK=True


class MainFrame(wx.Frame, TwainBase):
    """wxPython implementation of the simple demonstration"""
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
        wx.DefaultPosition, wx.Size(400,300))
        self.CreateStatusBar()
        menu = wx.Menu()        
        menu.Append(ID_OPEN_SCANNER, "&Connect", "Connect to the Scanner")
        menu.Append(ID_ACQUIRE_NATIVELY, "Acquire &Natively", "Acquire an Image using Native Transfer Interface")
        menu.Append(ID_ACQUIRE_BY_FILE, "Acquire By &File", "Acquire an Image using File Transfer Interface")
        menu.AppendSeparator()
        menu.Append(ID_EXIT, "E&xit", "Terminate the program")
        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self, ID_EXIT, self.MnuQuit)
        wx.EVT_MENU(self, ID_OPEN_SCANNER, self.MnuOpenScanner)
        wx.EVT_MENU(self, ID_ACQUIRE_NATIVELY, self.MnuAcquireNatively)
        wx.EVT_MENU(self, ID_ACQUIRE_BY_FILE, self.MnuAcquireByFile)
        wx.EVT_CLOSE(self, self.OnClose)

        self.scrolledWindow1 = wx.ScrolledWindow(id = ID_SCROLLEDWINDOW1, name = 'scrolledWindow1', parent = self, pos = wx.Point(0, 0), style = wx.TAB_TRAVERSAL | wx.SUNKEN_BORDER)
        self.bmpImage = wx.StaticBitmap(bitmap = wx.NullBitmap, id = ID_BMPIMAGE, name = 'bmpImage', parent = self.scrolledWindow1, pos = wx.Point(0, 0), style = 0)

        # Print out the exception - requires that you run from the command prompt
        sys.excepthook = traceback.print_exception

        # Initialise the Twain Base Class
        self.Initialise()

        # Polling based example
        if not USE_CALLBACK:
            wx.EVT_TIMER(self, ID_TIMER, self.onIdleTimer)
            self.timer=wx.Timer(self, ID_TIMER)
            self.timer.Start(250)

    def MnuQuit(self, event):
        self.Close(1)

    def OnClose(self, event):
        # Terminate the Twain Base Class
        self.Terminate()
        self.Destroy()

    def MnuOpenScanner(self, event):
        self.OpenScanner(self.GetHandle(), ProductName="Simple wxPython Demo", UseCallback=USE_CALLBACK)

    def MnuAcquireNatively(self, event):
        return self.AcquireNatively()

    def MnuAcquireByFile(self, event):
        return self.AcquireByFile()

    def DisplayImage(self, ImageFileName):
        bmp = wx.Image(ImageFileName, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.bmpImage.SetBitmap(bmp)
        self.scrolledWindow1.maxWidth = bmp.GetWidth()
        self.scrolledWindow1.maxHeight = bmp.GetHeight()
        self.scrolledWindow1.SetScrollbars(20, 20, bmp.GetWidth()/20, bmp.GetHeight()/20)
        self.bmpImage.Refresh()

    def LogMessage(self, message):
        # Set the title on the main window - used for tracing
        self.SetTitle(message)

    def onIdleTimer(self, event=None):
        """This is a polling mechanism. Get the image without relying on the callback."""
        self.PollForImage()

class SimpleApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1, "Simple TWAIN Demo")
        frame.Show(True)
        self.SetTopWindow(frame)
        return 1

SimpleApp(0).MainLoop()
 
