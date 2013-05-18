#Boa:Dialog:wxDialog1

import wx
import dlgLayout

def create(parent):
    return wxDialog1(parent)

[wxID_WXDIALOG1, wxID_WXDIALOG1BUTTON1, wxID_WXDIALOG1BUTTON2, wxID_WXDIALOG1BUTTON3, wxID_WXDIALOG1CBMODAL, wxID_WXDIALOG1CBSHOWUI] = [wx.NewId() for _init_ctrls in range(6)]

class wxDialog1(wx.Dialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id = wxID_WXDIALOG1, name = '', parent = prnt, pos = wx.Point(398, 267), size = wx.Size(379, 209), style=wx.DEFAULT_DIALOG_STYLE, title = 'Acquire Data from TWAIN Source')
        self._init_utils()
        self.SetClientSize(wx.Size(371, 182))

        self.button1 = wx.Button(id = wxID_WXDIALOG1BUTTON1, label = 'Acquire', name = 'button1', parent = self, pos = wx.Point(40, 120), size = wx.Size(75, 23), style = 0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button, id=wxID_WXDIALOG1BUTTON1)

        self.button2 = wx.Button(id = wxID_WXDIALOG1BUTTON2, label = 'Cancel', name = 'button2', parent = self, pos = wx.Point(144, 120), size = wx.Size(75, 23), style = 0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button, id=wxID_WXDIALOG1BUTTON2)

        self.cbShowUI = wx.CheckBox(id = wxID_WXDIALOG1CBSHOWUI, label = 'Show Source User Interface', name = 'cbShowUI', parent = self, pos = wx.Point(112, 40), size = wx.Size(160, 13), style = 0)
        self.cbShowUI.SetValue(False)

        self.cbModal = wx.CheckBox(id = wxID_WXDIALOG1CBMODAL, label = 'Source User Interface is Modal', name = 'cbModal', parent = self, pos = wx.Point(112, 80), size = wx.Size(176, 13), style = 0)
        self.cbModal.SetValue(False)

        self.button3 = wx.Button(id = wxID_WXDIALOG1BUTTON3, label = 'Layout', name = 'button3', parent = self, pos = wx.Point(248, 120), size = wx.Size(75, 23), style = 0)
        self.button3.Bind(wx.EVT_BUTTON, self.OnButton3Button, id=wxID_WXDIALOG1BUTTON3)

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnButton1Button(self, event):
        try:
            self.Control.statusBar1.SetStatusText("5 - Aquisition Requested", 2)
            self.Control.statusBar1.SetStatusText("Acquring", 0)
            self.Control.Log("self.SS.RequestAcquire(%d, %d)" %
                (self.cbShowUI.GetValue(), self.cbModal.GetValue()))
            rv = self.SS.RequestAcquire(self.cbShowUI.GetValue(),
                self.cbModal.GetValue())
            self.EndModal(1)
        except:
            self.Control.DisplayException("self.SS.RequestAcquire()")
        if hasattr(self.SS, 'ModalLoop'):
            self.SS.ModalLoop()

    def OnButton2Button(self, event):
        self.EndModal(0)

    def SetSourceInfo(self, SS, Control):
        ### Pass in three pieces of information, the SS object,
        ### and the Controller object. The
        ### controller object is used to log messages
        ### and display tracebacks.
        self.SS = SS
        self.Control = Control
        self.cbModal.SetValue(True)
        self.cbShowUI.SetValue(True)

    def OnButton3Button(self, event):
        self.Control.Log("self.SS.GetImageLayout()")
        try:
            Layout = self.SS.GetImageLayout()
        except:
            self.Control.DisplayException("self.SS.GetImageLayout")
            return
        (frame, DocNumber, PageNumber, FrameNumber) = Layout
        dlg = dlgLayout.create(self)
        try:
            dlg.SetLayout(frame[0],frame[1],frame[2],frame[3])
            rv = dlg.ShowModal()
            if rv:
                self.Control.Log("self.SS.SetImageLayout((%f, %f, %f, %f), %d, %d, %d)" %
                    (dlg.Left, dlg.Top, dlg.Right, dlg.Bottom,
                    DocNumber, PageNumber, FrameNumber))
                self.SS.SetImageLayout(
                    (dlg.Left, dlg.Top, dlg.Right, dlg.Bottom),
                    DocNumber, PageNumber, FrameNumber)
        except:
            self.Control.DisplayException("self.SS.SetImageLayout")
        dlg.Destroy()
