#Boa:Dialog:wxDialog1

import wx

import dlgFileXFer
#import dlgViewXfer
import twain
import frmViewBmp

def create(parent):
    return wxDialog1(parent)

[wxID_WXDIALOG1, wxID_WXDIALOG1BUTTON1, wxID_WXDIALOG1BUTTON2, 
 wxID_WXDIALOG1BUTTON3, wxID_WXDIALOG1STATICBOX1, wxID_WXDIALOG1STATICBOX2, 
 wxID_WXDIALOG1STATICBOX3, wxID_WXDIALOG1STATICTEXT1, 
 wxID_WXDIALOG1STATICTEXT10, wxID_WXDIALOG1STATICTEXT11, 
 wxID_WXDIALOG1STATICTEXT12, wxID_WXDIALOG1STATICTEXT13, 
 wxID_WXDIALOG1STATICTEXT14, wxID_WXDIALOG1STATICTEXT15, 
 wxID_WXDIALOG1STATICTEXT16, wxID_WXDIALOG1STATICTEXT17, 
 wxID_WXDIALOG1STATICTEXT18, wxID_WXDIALOG1STATICTEXT2, 
 wxID_WXDIALOG1STATICTEXT3, wxID_WXDIALOG1STATICTEXT4, 
 wxID_WXDIALOG1STATICTEXT5, wxID_WXDIALOG1STATICTEXT6, 
 wxID_WXDIALOG1STATICTEXT7, wxID_WXDIALOG1STATICTEXT8, 
 wxID_WXDIALOG1STATICTEXT9, wxID_WXDIALOG1TXTBITSPERPIXEL, 
 wxID_WXDIALOG1TXTBITSPERSAMPLE, wxID_WXDIALOG1TXTBOTTOM, 
 wxID_WXDIALOG1TXTCOMPRESSION, wxID_WXDIALOG1TXTDOCUMENTNUMBER, 
 wxID_WXDIALOG1TXTFRAMENUMBER, wxID_WXDIALOG1TXTIMAGELENGTH, 
 wxID_WXDIALOG1TXTIMAGEWIDTH, wxID_WXDIALOG1TXTLEFT, 
 wxID_WXDIALOG1TXTPAGENUMBER, wxID_WXDIALOG1TXTPIXELTYPE, 
 wxID_WXDIALOG1TXTPLANAR, wxID_WXDIALOG1TXTRIGHT, 
 wxID_WXDIALOG1TXTSAMPLESPERPIXEL, wxID_WXDIALOG1TXTTOP, 
 wxID_WXDIALOG1TXTXRESOLUTION, wxID_WXDIALOG1TXTYRESOLUTION, 
] = [wx.NewId() for _init_ctrls in range(42)]

class wxDialog1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_WXDIALOG1, name='', parent=prnt,
              pos=wx.Point(333, 110), size=wx.Size(558, 437),
              style=wx.DEFAULT_DIALOG_STYLE, title='Transfer Dialog')
        self.SetClientSize(wx.Size(550, 403))

        self.staticText1 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT1,
              label='Source Indicates that your requested data is now available.',
              name='staticText1', parent=self, pos=wx.Point(80, 16),
              size=wx.Size(415, 20), style=0)
        self.staticText1.SetForegroundColour(wx.Colour(255, 0, 0))
        self.staticText1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Sans Serif'))
        self.staticText1.SetBackgroundColour(wx.Colour(0, 255, 255))

        self.button1 = wx.Button(id=wxID_WXDIALOG1BUTTON1,
              label='Transfer Natively', name='button1', parent=self,
              pos=wx.Point(56, 344), size=wx.Size(112, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_WXDIALOG1BUTTON1)

        self.button2 = wx.Button(id=wxID_WXDIALOG1BUTTON2,
              label='Transfer To File', name='button2', parent=self,
              pos=wx.Point(208, 344), size=wx.Size(112, 23), style=0)
        self.button2.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_WXDIALOG1BUTTON2)

        self.button3 = wx.Button(id=wxID_WXDIALOG1BUTTON3,
              label='Abort Transfer', name='button3', parent=self,
              pos=wx.Point(360, 344), size=wx.Size(112, 23), style=0)
        self.button3.Bind(wx.EVT_BUTTON, self.OnButton3Button,
              id=wxID_WXDIALOG1BUTTON3)

        self.staticText2 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT2,
              label='X-Resolution:', name='staticText2', parent=self,
              pos=wx.Point(72, 64), size=wx.Size(63, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT3,
              label='Y-Resolution:', name='staticText3', parent=self,
              pos=wx.Point(72, 88), size=wx.Size(63, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT4,
              label='Image Width:', name='staticText4', parent=self,
              pos=wx.Point(72, 112), size=wx.Size(63, 13), style=0)

        self.staticText5 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT5,
              label='Image Length:', name='staticText5', parent=self,
              pos=wx.Point(64, 136), size=wx.Size(68, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT6,
              label='Samples Per Pixel:', name='staticText6', parent=self,
              pos=wx.Point(48, 160), size=wx.Size(87, 13), style=0)

        self.staticText7 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT7,
              label='Bits Per Sample:', name='staticText7', parent=self,
              pos=wx.Point(56, 184), size=wx.Size(77, 13), style=0)

        self.staticText8 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT8,
              label='Bits Per Pixel:', name='staticText8', parent=self,
              pos=wx.Point(64, 208), size=wx.Size(64, 13), style=0)

        self.staticText9 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT9,
              label='Planar:', name='staticText9', parent=self, pos=wx.Point(96,
              232), size=wx.Size(33, 13), style=0)

        self.staticText10 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT10,
              label='Pixel Type:', name='staticText10', parent=self,
              pos=wx.Point(72, 256), size=wx.Size(52, 13), style=0)

        self.staticText11 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT11,
              label='Compression:', name='staticText11', parent=self,
              pos=wx.Point(64, 280), size=wx.Size(63, 13), style=0)

        self.txtXResolution = wx.TextCtrl(id=wxID_WXDIALOG1TXTXRESOLUTION,
              name='txtXResolution', parent=self, pos=wx.Point(160, 64),
              size=wx.Size(100, 21), style=0, value='')

        self.txtYResolution = wx.TextCtrl(id=wxID_WXDIALOG1TXTYRESOLUTION,
              name='txtYResolution', parent=self, pos=wx.Point(160, 88),
              size=wx.Size(100, 21), style=0, value='')

        self.txtImageWidth = wx.TextCtrl(id=wxID_WXDIALOG1TXTIMAGEWIDTH,
              name='txtImageWidth', parent=self, pos=wx.Point(160, 112),
              size=wx.Size(100, 21), style=0, value='')

        self.txtImageLength = wx.TextCtrl(id=wxID_WXDIALOG1TXTIMAGELENGTH,
              name='txtImageLength', parent=self, pos=wx.Point(160, 136),
              size=wx.Size(100, 21), style=0, value='')

        self.txtSamplesPerPixel = wx.TextCtrl(id=wxID_WXDIALOG1TXTSAMPLESPERPIXEL,
              name='txtSamplesPerPixel', parent=self, pos=wx.Point(160, 160),
              size=wx.Size(100, 21), style=0, value='')

        self.txtBitsPerSample = wx.TextCtrl(id=wxID_WXDIALOG1TXTBITSPERSAMPLE,
              name='txtBitsPerSample', parent=self, pos=wx.Point(160, 184),
              size=wx.Size(100, 21), style=0, value='')

        self.txtBitsPerPixel = wx.TextCtrl(id=wxID_WXDIALOG1TXTBITSPERPIXEL,
              name='txtBitsPerPixel', parent=self, pos=wx.Point(160, 208),
              size=wx.Size(100, 21), style=0, value='')

        self.txtPlanar = wx.TextCtrl(id=wxID_WXDIALOG1TXTPLANAR,
              name='txtPlanar', parent=self, pos=wx.Point(160, 232),
              size=wx.Size(100, 21), style=0, value='')

        self.txtPixelType = wx.TextCtrl(id=wxID_WXDIALOG1TXTPIXELTYPE,
              name='txtPixelType', parent=self, pos=wx.Point(160, 256),
              size=wx.Size(100, 21), style=0, value='')

        self.txtCompression = wx.TextCtrl(id=wxID_WXDIALOG1TXTCOMPRESSION,
              name='txtCompression', parent=self, pos=wx.Point(160, 280),
              size=wx.Size(100, 21), style=0, value='')

        self.txtDocumentNumber = wx.TextCtrl(id=wxID_WXDIALOG1TXTDOCUMENTNUMBER,
              name='txtDocumentNumber', parent=self, pos=wx.Point(408, 64),
              size=wx.Size(100, 21), style=0, value='')

        self.staticText12 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT12,
              label='Document Number:', name='staticText12', parent=self,
              pos=wx.Point(304, 72), size=wx.Size(92, 13), style=0)

        self.txtPageNumber = wx.TextCtrl(id=wxID_WXDIALOG1TXTPAGENUMBER,
              name='txtPageNumber', parent=self, pos=wx.Point(408, 96),
              size=wx.Size(100, 21), style=0, value='')

        self.staticText13 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT13,
              label='Page Number:', name='staticText13', parent=self,
              pos=wx.Point(320, 104), size=wx.Size(68, 13), style=0)

        self.txtFrameNumber = wx.TextCtrl(id=wxID_WXDIALOG1TXTFRAMENUMBER,
              name='txtFrameNumber', parent=self, pos=wx.Point(408, 128),
              size=wx.Size(100, 21), style=0, value='')

        self.staticText18 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT18,
              label='Frame Number:', name='staticText18', parent=self,
              pos=wx.Point(320, 128), size=wx.Size(72, 13), style=0)

        self.txtLeft = wx.TextCtrl(id=wxID_WXDIALOG1TXTLEFT, name='txtLeft',
              parent=self, pos=wx.Point(408, 184), size=wx.Size(100, 21),
              style=0, value='')

        self.staticText14 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT14,
              label='Left:', name='staticText14', parent=self, pos=wx.Point(376,
              192), size=wx.Size(21, 13), style=0)

        self.txtTop = wx.TextCtrl(id=wxID_WXDIALOG1TXTTOP, name='txtTop',
              parent=self, pos=wx.Point(408, 216), size=wx.Size(100, 21),
              style=0, value='')

        self.staticText15 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT15,
              label='Top:', name='staticText15', parent=self, pos=wx.Point(376,
              216), size=wx.Size(22, 13), style=0)

        self.txtRight = wx.TextCtrl(id=wxID_WXDIALOG1TXTRIGHT, name='txtRight',
              parent=self, pos=wx.Point(408, 248), size=wx.Size(100, 21),
              style=0, value='')

        self.staticText16 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT16,
              label='Right', name='staticText16', parent=self, pos=wx.Point(368,
              248), size=wx.Size(25, 13), style=0)

        self.txtBottom = wx.TextCtrl(id=wxID_WXDIALOG1TXTBOTTOM,
              name='txtBottom', parent=self, pos=wx.Point(408, 280),
              size=wx.Size(100, 21), style=0, value='')

        self.staticText17 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT17,
              label='Bottom:', name='staticText17', parent=self,
              pos=wx.Point(360, 280), size=wx.Size(36, 13), style=0)

        self.staticBox1 = wx.StaticBox(id=wxID_WXDIALOG1STATICBOX1,
              label='Dimensions', name='staticBox1', parent=self,
              pos=wx.Point(312, 168), size=wx.Size(216, 152), style=0)

        self.staticBox2 = wx.StaticBox(id=wxID_WXDIALOG1STATICBOX2,
              label='Scan Information', name='staticBox2', parent=self,
              pos=wx.Point(24, 40), size=wx.Size(256, 280), style=0)

        self.staticBox3 = wx.StaticBox(id=wxID_WXDIALOG1STATICBOX3,
              label='Document Information', name='staticBox3', parent=self,
              pos=wx.Point(296, 48), size=wx.Size(232, 112), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        self.ShowMoreToCome(0)
        try:
            self.Control.Log("self.SS.XferImageNatively()")
            self.Control.statusBar1.SetStatusText("7 - Transferring Data", 2)
            (handle, more_to_come) = self.SS.XferImageNatively()
            self.Control.Log(">> (0x%lx, %d)"%(handle, more_to_come))
            if more_to_come:
                self.Control.statusBar1.SetStatusText("6 - Data Available", 2)
            else:
                self.Control.statusBar1.SetStatusText("5 - Acquisition Requested", 2)
            frm=frmViewBmp.create(self)
            frm.SetImageFile(handle, self.Control)
            self.Control.Log("twain.GlobalHandleFree(0x%lx)"%handle)
            twain.GlobalHandleFree(handle)
            frm.Show(1)
            frm.Raise()
            if more_to_come:
                self.ShowMoreToCome(1)
            else:
                # Provide from variable, so parent can re-raise it
                self.frm = frm
                self.Close(1)
        except:
            self.Control.DisplayException("self.SS.XferImageNatively")

    def ShowMoreToCome(self, bMoreAvailable):
        if bMoreAvailable:
            self.staticText1.SetLabel("Source Indicates that more data is available.")
        else:
            self.staticText1.SetLabel("")
        self.staticText1.Refresh()


    def OnButton2Button(self, event):
        self.ShowMoreToCome(0)
        GetXferFileNameWorks=False
        XferFileName=''
        try:
            self.Control.Log("self.SS.GetXferFileName()")
            (name, imgType) = self.SS.GetXferFileName()
            XferFileName=name
            GetXferFileNameWorks=True
        except:
            self.Control.Log("** This scanner does not support GetXferFileName - using default TWAIN.TMP")
            self.Control.DisplayException("self.SS.GetXferFileName()")
            (name, imgType) = ("twain.tmp", twain.TWFF_BMP)
            XferFileName='twain.tmp'

        if GetXferFileNameWorks:
            dlg = dlgFileXFer.create(self)
            dlg.SetInfo(name, imgType)
            try:
                rv = dlg.ShowModal()
                if rv:
                    self.Control.Log("self.SS.SetXferFileName('%s', %d)" % (dlg.Name, dlg.imgType))
                    if dlg.Name:
                        self.SS.SetXferFileName(dlg.Name, dlg.imgType)
                        XferFileName=dlg.Name
            except:
                self.Control.DisplayException("self.SS.SetXferFileName")
            dlg.Destroy()

        try:
            self.Control.Log("self.SS.XferImageByFile()")
            self.Control.statusBar1.SetStatusText("7 - Transferring Data", 2)
            more_to_come = self.SS.XferImageByFile()
            self.Control.Log(">> %d"%more_to_come)

            # Display the image, assume Bitmap
            frm=frmViewBmp.create(self)
            frm.SetImageFromFile(XferFileName, self)
            frm.Show(1)
            frm.Raise()
            self.FileViewer = frm
            
            # Let the user know the operation was successful
            if more_to_come:
                self.Control.statusBar1.SetStatusText("6 - Data Available", 2)
            else:
                self.Control.statusBar1.SetStatusText("4 - Source Open", 2)
                self.Control.statusBar1.SetStatusText("Aquisition Complete", 0)

            if more_to_come:
                self.ShowMoreToCome(1)
            else:
                self.Close(1)
            
        except:
            self.Control.DisplayException("self.SS.XferImageByFile")

    def OnButton3Button(self, event):
        ### Abort transfer
        self.ShowMoreToCome(0)
        try:
            self.Control.Log("self.SS.CancelAllPendingXfers()")
            self.SS.CancelAllPendingXfers()
            self.Close(1)
        except:
            self.Control.DisplayException("self.SS.CancelAllPendingXfers()")

    def SetSourceInfo(self, SS, Control):
        ### Pass in three pieces of information, the SS object,
        ### the Capability Name and the Controller object. The
        ### controller object is used to log messages
        ### and display tracebacks.
        self.SS = SS
        self.Control = Control
        self.DisplaySourceData()

    def DisplaySourceData(self):
        ## Get the Image Information and Display
        try:
            self.Control.Log("self.SS.GetImageInfo()")
            info = self.SS.GetImageInfo()
        except:
            self.Control.Log("Exception raised [%s]" % str(sys.exc_info()))
            info = None ## Audio ?
        if info:
            self.txtXResolution.SetValue(str(info['XResolution']))
            self.txtYResolution .SetValue(str(info['YResolution']))
            self.txtImageWidth.SetValue(str(info['ImageWidth']))
            self.txtImageLength.SetValue(str(info['ImageLength']))
            self.txtSamplesPerPixel.SetValue(str(info['SamplesPerPixel']))
            self.txtBitsPerSample.SetValue(str(info['BitsPerSample']))
            self.txtBitsPerPixel.SetValue(str(info['BitsPerPixel']))
            self.txtPlanar.SetValue(str(info['Planar']))
            self.txtPixelType.SetValue(str(info['PixelType']))
            self.txtCompression.SetValue(str(info['Compression']))
        try:
            self.Control.Log("self.SS.GetImageLayout()")
            Layout = self.SS.GetImageLayout()
        except:
            self.Control.Log("Exception raised [%s]" % str(sys.exc_info()))
            Layout = None ## Audio ?
        if Layout:
            (frame, DocNumber, PageNumber, FrameNumber) = Layout
            self.txtDocumentNumber.SetValue(str(DocNumber))
            self.txtPageNumber.SetValue(str(PageNumber))
            self.txtFrameNumber.SetValue(str(FrameNumber))
            self.txtLeft.SetValue(str(frame[0]))
            self.txtTop.SetValue(str(frame[1]))
            self.txtRight.SetValue(str(frame[2]))
            self.txtBottom.SetValue(str(frame[3]))
