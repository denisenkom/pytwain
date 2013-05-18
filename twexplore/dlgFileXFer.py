#Boa:Dialog:wxDialog1

import wx

import twain

def create(parent):
    return wxDialog1(parent)

[wxID_WXDIALOG1, wxID_WXDIALOG1BUTTON1, wxID_WXDIALOG1BUTTON2, wxID_WXDIALOG1CHOICEFILEFORMAT, wxID_WXDIALOG1STATICTEXT1, wxID_WXDIALOG1STATICTEXT2, wxID_WXDIALOG1TXTFILENAME] = [wx.NewId() for _init_ctrls in range(7)]

class wxDialog1(wx.Dialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id = wxID_WXDIALOG1, name = '', parent = prnt, pos = wx.Point(479, 193), size = wx.Size(442, 222), style=wx.DEFAULT_DIALOG_STYLE, title = 'Transfer By File')
        self._init_utils()
        self.SetClientSize(wx.Size(434, 195))

        self.staticText1 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT1, label = 'Target File Name:', name = 'staticText1', parent = self, pos = wx.Point(48, 32), size = wx.Size(84, 13), style = 0)

        self.staticText2 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT2, label = 'File Format:', name = 'staticText2', parent = self, pos = wx.Point(80, 64), size = wx.Size(54, 13), style = 0)

        self.button1 = wx.Button(id = wxID_WXDIALOG1BUTTON1, label = 'Get Image', name = 'button1', parent = self, pos = wx.Point(112, 136), size = wx.Size(75, 23), style = 0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button, id=wxID_WXDIALOG1BUTTON1)

        self.button2 = wx.Button(id = wxID_WXDIALOG1BUTTON2, label = 'Cancel', name = 'button2', parent = self, pos = wx.Point(240, 136), size = wx.Size(75, 23), style = 0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button, id=wxID_WXDIALOG1BUTTON2)

        self.txtFileName = wx.TextCtrl(id = wxID_WXDIALOG1TXTFILENAME, name = 'txtFileName', parent = self, pos = wx.Point(144, 32), size = wx.Size(264, 21), style = 0, value = '')

        self.choiceFileFormat = wx.Choice(choices = [], id = wxID_WXDIALOG1CHOICEFILEFORMAT, name = 'choiceFileFormat', parent = self, pos = wx.Point(144, 64), size = wx.Size(192, 21), style = 0, validator = wx.DefaultValidator)

    def __init__(self, parent):
        self._init_ctrls(parent)

        # Populate the combo box from the options
        self.choiceFileFormat.Clear()
        for i in [ i for i in dir(twain) if i[:5] == 'TWFF_' ]:
            self.choiceFileFormat.Append(i)

    def LookupFormatName(self, id):
        for i in [ i for i in dir(twain) if i[:5] == 'TWFF_' ]:
            value = getattr(twain, i)
            if value == id: return i
        return 'Unknown'

    def OnButton1Button(self, event):
        self.Name = self.txtFileName.GetValue()
        self.imgType = getattr(twain, self.choiceFileFormat.GetStringSelection())
        self.EndModal(1)

    def OnButton2Button(self, event):
        self.EndModal(0)

    def SetInfo(self, name, imgType):
        self.txtFileName.SetValue(name)
        try:
            s= self.LookupFormatName(imgType)
            self.choiceFileFormat.SetStringSelection(s)
        except:
            pass
