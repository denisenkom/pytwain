#Boa:Dialog:wxDialog1

import wx

def create(parent):
    return wxDialog1(parent)

[wxID_WXDIALOG1, wxID_WXDIALOG1BUTTON1, wxID_WXDIALOG1BUTTON2, 
 wxID_WXDIALOG1STATICTEXT1, wxID_WXDIALOG1STATICTEXT2, 
 wxID_WXDIALOG1STATICTEXT3, wxID_WXDIALOG1STATICTEXT4, 
 wxID_WXDIALOG1TXTBOTTOM, wxID_WXDIALOG1TXTLEFT, wxID_WXDIALOG1TXTRIGHT, 
 wxID_WXDIALOG1TXTTOP, 
] = [wx.NewId() for _init_ctrls in range(11)]

class wxDialog1(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_WXDIALOG1, name='', parent=prnt,
              pos=wx.Point(471, 209), size=wx.Size(357, 279),
              style=wx.DEFAULT_DIALOG_STYLE, title='Select Image Frame')
        self.SetClientSize(wx.Size(349, 245))

        self.staticText1 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT1,
              label='Left:', name='staticText1', parent=self, pos=wx.Point(80,
              32), size=wx.Size(21, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT2,
              label='Top:', name='staticText2', parent=self, pos=wx.Point(80,
              64), size=wx.Size(22, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT3,
              label='Right:', name='staticText3', parent=self, pos=wx.Point(80,
              96), size=wx.Size(28, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID_WXDIALOG1STATICTEXT4,
              label='Bottom:', name='staticText4', parent=self, pos=wx.Point(72,
              128), size=wx.Size(36, 13), style=0)

        self.txtLeft = wx.TextCtrl(id=wxID_WXDIALOG1TXTLEFT, name='txtLeft',
              parent=self, pos=wx.Point(120, 32), size=wx.Size(100, 21),
              style=0, value='')

        self.txtTop = wx.TextCtrl(id=wxID_WXDIALOG1TXTTOP, name='txtTop',
              parent=self, pos=wx.Point(120, 64), size=wx.Size(100, 21),
              style=0, value='')

        self.txtRight = wx.TextCtrl(id=wxID_WXDIALOG1TXTRIGHT, name='txtRight',
              parent=self, pos=wx.Point(120, 96), size=wx.Size(100, 21),
              style=0, value='')

        self.txtBottom = wx.TextCtrl(id=wxID_WXDIALOG1TXTBOTTOM,
              name='txtBottom', parent=self, pos=wx.Point(120, 128),
              size=wx.Size(100, 21), style=0, value='')

        self.button1 = wx.Button(id=wxID_WXDIALOG1BUTTON1, label='Update',
              name='button1', parent=self, pos=wx.Point(64, 192),
              size=wx.Size(75, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_WXDIALOG1BUTTON1)

        self.button2 = wx.Button(id=wxID_WXDIALOG1BUTTON2, label='Cancel',
              name='button2', parent=self, pos=wx.Point(192, 192),
              size=wx.Size(75, 23), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_WXDIALOG1BUTTON2)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        self.Left = float(self.txtLeft.GetValue())
        self.Top = float(self.txtTop.GetValue())
        self.Right = float(self.txtRight.GetValue())
        self.Bottom = float(self.txtBottom.GetValue())
        self.EndModal(1)

    def OnButton2Button(self, event):
        self.EndModal(0)

    def SetLayout(self, left, top, right, bottom):
        self.txtLeft.SetValue(str(left))
        self.txtTop.SetValue(str(top))
        self.txtRight.SetValue(str(right))
        self.txtBottom.SetValue(str(bottom) )
