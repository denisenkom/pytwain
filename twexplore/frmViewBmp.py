#Boa:Frame:wxFrame2

import wx
from wx.lib.anchors import LayoutAnchors

import os

import twain

TmpFileName="temp.bmp"

def create(parent):
    return wxFrame2(parent)

[wxID_WXFRAME2, wxID_WXFRAME2BMPIMAGE, wxID_WXFRAME2SCROLLEDWINDOW1, 
] = [wx.NewId() for _init_ctrls in range(3)]

class wxFrame2(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_WXFRAME2, name='', parent=prnt,
              pos=wx.Point(2, 2), size=wx.Size(649, 684),
              style=wx.DEFAULT_FRAME_STYLE, title='View Image as BIT Map')
        self.SetClientSize(wx.Size(641, 650))

        self.scrolledWindow1 = wx.ScrolledWindow(id=wxID_WXFRAME2SCROLLEDWINDOW1,
              name='scrolledWindow1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(641, 650), style=wx.TAB_TRAVERSAL)
        self.scrolledWindow1.SetConstraints(LayoutAnchors(self.scrolledWindow1,
              True, True, True, True))
        self.scrolledWindow1.SetAutoLayout(True)

        self.bmpImage = wx.StaticBitmap(bitmap=wx.NullBitmap,
              id=wxID_WXFRAME2BMPIMAGE, name='bmpImage',
              parent=self.scrolledWindow1, pos=wx.Point(0, 0), size=wx.Size(640,
              648), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def SetImageFile(self, handle, Control):
        self.Control = Control
        try:
            self.Control.Log("twain.DIBToBMFile(0x%lx, '%s')" % (handle, TmpFileName))
            twain.DIBToBMFile(handle, TmpFileName)
        except:
            self.Control.DisplayException("twain.DIBToBMFile()")
            return
        try:
            FileSize = int(os.stat(TmpFileName)[6] / 1000)
            self.SetTitle("View Image : %s [File Size = %dk]" % (TmpFileName, FileSize))
            bmp = wx.Image(TmpFileName, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
            self.bmpImage.SetBitmap(bmp)
            self.scrolledWindow1.maxWidth = bmp.GetWidth()
            self.scrolledWindow1.maxHeight = bmp.GetHeight()
            self.scrolledWindow1.SetScrollbars(20, 20, bmp.GetWidth()/20, bmp.GetHeight()/20)
            self.bmpImage.Refresh()
        except:
            self.Control.DisplayException("View Bitmap")

    def SetImageFromFile(self, FileName, Control):
        self.Control = Control
        try:
            FileSize = int(os.stat(FileName)[6] / 1000)
            self.SetTitle("View Image : %s [File Size = %dk]" % (FileName, FileSize))
            ##bmp = wx.Image(FileName, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
            bmp = wx.Bitmap(FileName, wx.BITMAP_TYPE_BMP)
            self.bmpImage.SetBitmap(bmp)
            self.scrolledWindow1.maxWidth = bmp.GetWidth()
            self.scrolledWindow1.maxHeight = bmp.GetHeight()
            self.scrolledWindow1.SetScrollbars(20, 20, bmp.GetWidth()/20, bmp.GetHeight()/20)
            self.bmpImage.Refresh()
        except:
            self.Control.DisplayException("View Bitmap")
            
