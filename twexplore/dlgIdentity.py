#Boa:Dialog:wxDialog1

import wx

import twain

def create(parent):
    return wxDialog1(parent)

[wxID_WXDIALOG1, wxID_WXDIALOG1BUTTON1, wxID_WXDIALOG1STATICBOX1, wxID_WXDIALOG1STATICBOX2, wxID_WXDIALOG1STATICTEXT1, wxID_WXDIALOG1STATICTEXT10, wxID_WXDIALOG1STATICTEXT11, wxID_WXDIALOG1STATICTEXT2, wxID_WXDIALOG1STATICTEXT3, wxID_WXDIALOG1STATICTEXT4, wxID_WXDIALOG1STATICTEXT5, wxID_WXDIALOG1STATICTEXT6, wxID_WXDIALOG1STATICTEXT7, wxID_WXDIALOG1STATICTEXT8, wxID_WXDIALOG1STATICTEXT9, wxID_WXDIALOG1TXTCOUNTRY, wxID_WXDIALOG1TXTINFO, wxID_WXDIALOG1TXTLANGUAGE, wxID_WXDIALOG1TXTMANUFACTURER, wxID_WXDIALOG1TXTPRODUCTFAMILY, wxID_WXDIALOG1TXTPRODUCTNAME, wxID_WXDIALOG1TXTPROTOCOLMAJOR, wxID_WXDIALOG1TXTPROTOCOLMINOR, wxID_WXDIALOG1TXTSUPPORTEDGROUPS, wxID_WXDIALOG1TXTVERMAJOR, wxID_WXDIALOG1TXTVERMINOR] = [wx.NewId() for _init_ctrls in range(26)]

class wxDialog1(wx.Dialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id = wxID_WXDIALOG1, name = '', parent = prnt, pos = wx.Point(365, 52), size = wx.Size(438, 537), style=wx.DEFAULT_DIALOG_STYLE, title = 'Driver Information')
        self._init_utils()
        self.SetClientSize(wx.Size(430, 510))

        self.staticBox1 = wx.StaticBox(id = wxID_WXDIALOG1STATICBOX1, label = '', name = 'staticBox1', parent = self, pos = wx.Point(16, 16), size = wx.Size(384, 216), style = 0)

        self.staticBox2 = wx.StaticBox(id = wxID_WXDIALOG1STATICBOX2, label = 'V ersion', name = 'staticBox2', parent = self, pos = wx.Point(16, 248), size = wx.Size(384, 184), style = 0)

        self.staticText1 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT1, label = 'Product Name:', name = 'staticText1', parent = self, pos = wx.Point(88, 40), size = wx.Size(71, 13), style = 0)

        self.staticText2 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT2, label = 'Protocol Major:', name = 'staticText2', parent = self, pos = wx.Point(88, 72), size = wx.Size(71, 13), style = 0)

        self.staticText3 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT3, label = 'Protocol Minor:', name = 'staticText3', parent = self, pos = wx.Point(88, 104), size = wx.Size(71, 13), style = 0)

        self.staticText4 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT4, label = 'Supported Groups:', name = 'staticText4', parent = self, pos = wx.Point(72, 136), size = wx.Size(89, 13), style = 0)

        self.staticText5 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT5, label = 'Manufacturer:', name = 'staticText5', parent = self, pos = wx.Point(96, 168), size = wx.Size(66, 13), style = 0)

        self.staticText6 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT6, label = 'Product Family:', name = 'staticText6', parent = self, pos = wx.Point(88, 200), size = wx.Size(72, 13), style = 0)

        self.staticText7 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT7, label = 'Major Number:', name = 'staticText7', parent = self, pos = wx.Point(88, 272), size = wx.Size(69, 13), style = 0)

        self.staticText8 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT8, label = 'Minor Number:', name = 'staticText8', parent = self, pos = wx.Point(88, 304), size = wx.Size(69, 13), style = 0)

        self.staticText9 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT9, label = 'Language:', name = 'staticText9', parent = self, pos = wx.Point(104, 336), size = wx.Size(51, 13), style = 0)

        self.staticText10 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT10, label = 'Country:', name = 'staticText10', parent = self, pos = wx.Point(112, 368), size = wx.Size(39, 13), style = 0)

        self.staticText11 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT11, label = 'Info:', name = 'staticText11', parent = self, pos = wx.Point(128, 400), size = wx.Size(21, 13), style = 0)

        self.txtProductName = wx.TextCtrl(id = wxID_WXDIALOG1TXTPRODUCTNAME, name = 'txtProductName', parent = self, pos = wx.Point(168, 40), size = wx.Size(216, 21), style = 0, value = '')

        self.txtProtocolMajor = wx.TextCtrl(id = wxID_WXDIALOG1TXTPROTOCOLMAJOR, name = 'txtProtocolMajor', parent = self, pos = wx.Point(168, 72), size = wx.Size(100, 21), style = 0, value = '')

        self.txtProtocolMinor = wx.TextCtrl(id = wxID_WXDIALOG1TXTPROTOCOLMINOR, name = 'txtProtocolMinor', parent = self, pos = wx.Point(168, 104), size = wx.Size(100, 21), style = 0, value = '')

        self.txtSupportedGroups = wx.TextCtrl(id = wxID_WXDIALOG1TXTSUPPORTEDGROUPS, name = 'txtSupportedGroups', parent = self, pos = wx.Point(168, 136), size = wx.Size(216, 21), style = 0, value = '')

        self.txtManufacturer = wx.TextCtrl(id = wxID_WXDIALOG1TXTMANUFACTURER, name = 'txtManufacturer', parent = self, pos = wx.Point(168, 168), size = wx.Size(216, 21), style = 0, value = '')

        self.txtProductFamily = wx.TextCtrl(id = wxID_WXDIALOG1TXTPRODUCTFAMILY, name = 'txtProductFamily', parent = self, pos = wx.Point(168, 200), size = wx.Size(216, 21), style = 0, value = '')

        self.txtVerMajor = wx.TextCtrl(id = wxID_WXDIALOG1TXTVERMAJOR, name = 'txtVerMajor', parent = self, pos = wx.Point(168, 272), size = wx.Size(100, 21), style = 0, value = '')

        self.txtVerMinor = wx.TextCtrl(id = wxID_WXDIALOG1TXTVERMINOR, name = 'txtVerMinor', parent = self, pos = wx.Point(168, 304), size = wx.Size(100, 21), style = 0, value = '')

        self.txtLanguage = wx.TextCtrl(id = wxID_WXDIALOG1TXTLANGUAGE, name = 'txtLanguage', parent = self, pos = wx.Point(168, 336), size = wx.Size(176, 21), style = 0, value = '')

        self.txtCountry = wx.TextCtrl(id = wxID_WXDIALOG1TXTCOUNTRY, name = 'txtCountry', parent = self, pos = wx.Point(168, 368), size = wx.Size(100, 21), style = 0, value = '')

        self.txtInfo = wx.TextCtrl(id = wxID_WXDIALOG1TXTINFO, name = 'txtInfo', parent = self, pos = wx.Point(168, 400), size = wx.Size(216, 21), style = 0, value = '')

        self.button1 = wx.Button(id = wxID_WXDIALOG1BUTTON1, label = 'Close', name = 'button1', parent = self, pos = wx.Point(152, 456), size = wx.Size(75, 23), style = 0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button, id=wxID_WXDIALOG1BUTTON1)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        self.Close(0)

    def SetSourceInfo(self, Control, Identity):
        self.txtProductName.SetValue(str(Identity['ProductName']))
        self.txtProtocolMajor.SetValue(str(Identity['ProtocolMajor']))
        self.txtProtocolMinor.SetValue(str(Identity['ProtocolMinor']))
        sgs=""
        sgVal = Identity['SupportedGroups']
        if sgVal & twain.DG_CONTROL:
            if len(sgs): sgs= "DG_CONTROL"
            else: sgs=sgs + "|DG_CONTROL"
        if sgVal & twain.DG_IMAGE:
            if len(sgs): sgs= "DG_IMAGE"
            else: sgs=sgs + "|DG_IMAGE"
        if sgVal & twain.DG_AUDIO:
            if len(sgs): sgs= "DG_AUDIO"
            else: sgs=sgs + "|DG_AUDIO"
        self.txtSupportedGroups.SetValue(sgs)
        self.txtManufacturer.SetValue(str(Identity['Manufacturer']))
        self.txtProductFamily.SetValue(str(Identity['ProductFamily']))
        self.txtVerMajor.SetValue(str(Identity['MajorNum']))
        self.txtVerMinor.SetValue(str(Identity['MinorNum']))
        language_constant = Control.LookUpConstant("TWLG", Identity['Language'])
        if language_constant:
            self.txtLanguage.SetValue(language_constant)
        else:
            self.txtLanguage.SetValue(str(Identity['Language']))
        self.txtCountry.SetValue(str(Identity['Country']))
        self.txtInfo.SetValue(str(Identity['Info']))
