#Boa:Dialog:wxDialog1

import wx

import twain

def create(parent):
    return wxDialog1(parent)

[wxID_WXDIALOG1, wxID_WXDIALOG1BTNONEVALCANCEL, wxID_WXDIALOG1BTNONEVALRESET, wxID_WXDIALOG1BTNONEVALUPDATE, wxID_WXDIALOG1NOTEBOOK1, wxID_WXDIALOG1PANEL1, wxID_WXDIALOG1PANEL2, wxID_WXDIALOG1PANEL3, wxID_WXDIALOG1PANEL4, wxID_WXDIALOG1RBCAPABILITYTYPE, wxID_WXDIALOG1STATICTEXT1, wxID_WXDIALOG1TXTVALUE] = [wx.NewId() for _init_ctrls in range(12)]

class wxDialog1(wx.Dialog):
    def _init_coll_notebook1_Pages(self, parent):

        parent.AddPage(self.panel1, 'ONEVALUE', select = True, imageId = -1)
        parent.AddPage(self.panel2, 'ENUMERATION', select = False, imageId = -1)
        parent.AddPage(self.panel3, 'ARRAY', select = False, imageId = -1)
        parent.AddPage(self.panel4, 'RANGE', select = False, imageId = -1)

    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id = wxID_WXDIALOG1, name = '', parent = prnt, pos = wx.Point(357, 145), size = wx.Size(429, 369), style=wx.DEFAULT_DIALOG_STYLE, title = 'Change Capability')
        self._init_utils()
        self.SetClientSize(wx.Size(421, 342))

        self.notebook1 = wx.Notebook(id = wxID_WXDIALOG1NOTEBOOK1, name = 'notebook1', parent = self, pos = wx.Point(0, 0), size = wx.Size(421, 342), style = 0)

        self.panel1 = wx.Panel(id = wxID_WXDIALOG1PANEL1, name = 'panel1', parent = self.notebook1, pos = wx.Point(0, 0), size = wx.Size(413, 316), style=wx.TAB_TRAVERSAL)

        self.panel2 = wx.Panel(id = wxID_WXDIALOG1PANEL2, name = 'panel2', parent = self.notebook1, pos = wx.Point(0, 0), size = wx.Size(413, 316), style=wx.TAB_TRAVERSAL)

        self.panel3 = wx.Panel(id = wxID_WXDIALOG1PANEL3, name = 'panel3', parent = self.notebook1, pos = wx.Point(0, 0), size = wx.Size(413, 316), style=wx.TAB_TRAVERSAL)

        self.panel4 = wx.Panel(id = wxID_WXDIALOG1PANEL4, name = 'panel4', parent = self.notebook1, pos = wx.Point(0, 0), size = wx.Size(413, 316), style=wx.TAB_TRAVERSAL)

        self.staticText1 = wx.StaticText(id = wxID_WXDIALOG1STATICTEXT1, label = 'New Value:', name = 'staticText1', parent = self.panel1, pos = wx.Point(80, 40), size = wx.Size(55, 13), style = 0)

        self.txtValue = wx.TextCtrl(id = wxID_WXDIALOG1TXTVALUE, name = 'txtValue', parent = self.panel1, pos = wx.Point(152, 32), size = wx.Size(100, 21), style = 0, value = '')

        self.rbCapabilityType = wx.RadioBox(choices = ['TWTY_UINT32', 'TWTY_STR64', 'TWTY_UINT16', 'TWTY_BOOL', 'TWTY_INT32', 'TWTY_STR255', 'TWTY_STR128', 'TWTY_UINT8', 'TWTY_INT16', 'TWTY_INT8', 'TWTY_FIX32', 'TWTY_FRAME', 'TWTY_STR32'], id = wxID_WXDIALOG1RBCAPABILITYTYPE, label = 'Type of the Value', majorDimension = 3, name = 'rbCapabilityType', parent = self.panel1, point = wx.Point(40, 96), size = wx.Size(350, 128), style=wx.RA_SPECIFY_COLS, validator = wx.DefaultValidator)

        self.btnOneValUpdate = wx.Button(id = wxID_WXDIALOG1BTNONEVALUPDATE, label = 'Update Value', name = 'btnOneValUpdate', parent = self.panel1, pos = wx.Point(64, 272), size = wx.Size(75, 23), style = 0)
        self.btnOneValUpdate.Bind(wx.EVT_BUTTON, self.OnBtnonevalupdateButton, id=wxID_WXDIALOG1BTNONEVALUPDATE)

        self.btnOneValReset = wx.Button(id = wxID_WXDIALOG1BTNONEVALRESET, label = 'Reset Value', name = 'btnOneValReset', parent = self.panel1, pos = wx.Point(176, 272), size = wx.Size(75, 23), style = 0)
        self.btnOneValReset.Bind(wx.EVT_BUTTON, self.OnBtnonevalresetButton, id=wxID_WXDIALOG1BTNONEVALRESET)

        self.btnOneValCancel = wx.Button(id = wxID_WXDIALOG1BTNONEVALCANCEL, label = 'Close', name = 'btnOneValCancel', parent = self.panel1, pos = wx.Point(288, 272), size = wx.Size(75, 23), style = 0)
        self.btnOneValCancel.Bind(wx.EVT_BUTTON, self.OnBtnonevalcancelButton, id=wxID_WXDIALOG1BTNONEVALCANCEL)

        self._init_coll_notebook1_Pages(self.notebook1)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnBtnonevalupdateButton(self, event):
        value = self.txtValue.GetValue()
        format = self.rbCapabilityType.GetStringSelection()
        formatId = getattr(twain, format)
        try:
            self.Control.Log("self.SS.SetCapability(twain.%s, twain.%s, %s)" %
                (self.Name, format, value))
            if not format[0].isdigit():
                value = eval(value, twain.__dict__)  ## do not do this at home children
            elif format in ["TWTY_INT8","TWTY_INT16","TWTY_INT32","TWTY_UINT8","TWTY_UINT16",
                "TWTY_UINT32","TWTY_BOOL"]:
                value = int(value)
            elif format in ["TWTY_FIX32"]:
                value = float(value)
            elif format in ["TWTY_FRAME"]:
                value = eval(value)  ## do not do this at home children
            self.SS.SetCapability(self.CapId, getattr(twain, format), value)
            (capType, capVal) = self.SS.GetCapabilityCurrent(self.CapId)
            self.txtValue.SetValue(str(capVal))
        except:
            self.Control.DisplayException("self.SS.SetCapability")

    def OnBtnonevalresetButton(self, event):
        try:
            self.Control.Log("self.SS.ResetCapability(twain.%s)" % self.Name)
            self.SS.ResetCapability(self.CapId)
            (capType, capVal) = self.SS.GetCapabilityCurrent(self.CapId)
            self.txtValue.SetValue(str(capVal))
        except:
            self.Control.DisplayException("self.SS.ResetCapability")

    def OnBtnonevalcancelButton(self, event):
        self.EndModal(0)

    def SetSourceInfo(self, SS, Control, Name):
        ### Pass in three pieces of information, the SS object,
        ### the Capability Name and the Controller object. The
        ### controller object is used to get the typename, log messages
        ### and display tracebacks.
        self.SS = SS
        self.Name = Name
        self.Control = Control
        self.CapId = getattr(twain,Name)
        self.SetTitle("Set Capability: " + Name)
        self.notebook1.SetSelection(0)
        try:
            (capType, capVal) = SS.GetCapabilityCurrent(self.CapId)
            self.txtValue.SetValue(str(capVal))
            self.rbCapabilityType.SetStringSelection(Control.GetNameForType(capType))
        except:
            self.txtValue.SetValue("")
            self.rbCapabilityType.SetStringSelection("TWTY_UNIT16")
