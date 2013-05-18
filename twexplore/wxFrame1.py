#Boa:Frame:wxFrame1

import wx

import twain
import string, traceback, sys

import ChangeCap
import dlgAcquire
import dlgTransfer
import dlgIdentity
import twexplore

def create(parent):
    return wxFrame1(parent)

[wxID_WXFRAME1, wxID_WXFRAME1LISTCAPS, wxID_WXFRAME1SPLITTERWINDOW1, wxID_WXFRAME1STATUSBAR1, wxID_WXFRAME1TXTLOG] = [wx.NewId() for _init_ctrls in range(5)]

[wxID_WXFRAME1FILEMENUITEMS0, wxID_WXFRAME1FILEMENUITEMS1, wxID_WXFRAME1FILEMENUITEMS2, wxID_WXFRAME1FILEMENUITEMS3, wxID_WXFRAME1FILEMENUITEMS4] = [wx.NewId() for _init_coll_FileMenu_Items in range(5)]

class wxFrame1(wx.Frame):
    def _init_coll_FileMenu_Items(self, parent):

        parent.Append(wxID_WXFRAME1FILEMENUITEMS0, 'Connect', 'Connect to Scanner or other TWAIN device')
        parent.Append(wxID_WXFRAME1FILEMENUITEMS1, 'Disconnect', 'Disconnect From Scanner or TWAIN Device', )
        parent.Append(wxID_WXFRAME1FILEMENUITEMS2, 'Acquire', 'Acquire')
        parent.Append(wxID_WXFRAME1FILEMENUITEMS3, 'Refresh Capabilities', 'Refresh Capabilities', )
        parent.Append(wxID_WXFRAME1FILEMENUITEMS4, 'Exit', 'Exit the Program', )
        self.Bind(wx.EVT_MENU, self.OnFilemenuitems0Menu, id=wxID_WXFRAME1FILEMENUITEMS0)
        self.Bind(wx.EVT_MENU, self.OnFilemenuitems1Menu, id=wxID_WXFRAME1FILEMENUITEMS1)
        self.Bind(wx.EVT_MENU, self.OnFilemenuitems2Menu, id=wxID_WXFRAME1FILEMENUITEMS2)
        self.Bind(wx.EVT_MENU, self.OnFilemenuitems3Menu, id=wxID_WXFRAME1FILEMENUITEMS3)
        self.Bind(wx.EVT_MENU, self.OnFilemenuitems4Menu, id=wxID_WXFRAME1FILEMENUITEMS4)

    def _init_coll_menuBar1_Menus(self, parent):

        parent.Append(menu = self.FileMenu, title = 'File')

    def _init_coll_listCaps_Columns(self, parent):

        parent.InsertColumn(col = 0, format = wx.LIST_FORMAT_LEFT, heading = 'Capability', width = 200)
        parent.InsertColumn(col = 1, format = wx.LIST_FORMAT_LEFT, heading = 'Supported Values', width = 400)
        parent.InsertColumn(col = 2, format = wx.LIST_FORMAT_LEFT, heading = 'Current Value', width = 100)

    def _init_coll_statusBar1_Fields(self, parent):
        parent.SetFieldsCount(3)

        parent.SetStatusText(number=0, text = 'sbMessage')
        parent.SetStatusText(number=1, text = 'sbSource')
        parent.SetStatusText(number=2, text = 'sbStatus')

        parent.SetStatusWidths([-1, 200, 200])

    def _init_utils(self):
        self.menuBar1 = wx.MenuBar()

        self.FileMenu = wx.Menu(title = '')
        self._init_coll_FileMenu_Items(self.FileMenu)

        self._init_coll_menuBar1_Menus(self.menuBar1)

    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id = wxID_WXFRAME1, name = 'twexplore', parent = prnt, pos = wx.Point(254, 66), size = wx.Size(768, 537), style=wx.DEFAULT_FRAME_STYLE, title = 'TWAIN Explorer')
        self._init_utils()
        self.SetClientSize(wx.Size(760, 510))
        self.SetMenuBar(self.menuBar1)

        self.splitterWindow1 = wx.SplitterWindow(id = wxID_WXFRAME1SPLITTERWINDOW1, name = 'splitterWindow1', parent = self, point = wx.Point(128, -32), size = wx.Size(760, 491), style=wx.SP_3D)

        self.txtLog = wx.TextCtrl(id = wxID_WXFRAME1TXTLOG, name = 'txtLog', parent = self.splitterWindow1, pos = wx.Point(2, 387), size = wx.Size(756, 82), style=wx.TE_MULTILINE, value = '')
        #self.txtLog.SetTitle('')
        self.txtLog.SetLabel('')
        self.txtLog.SetToolTipString('LogWindow')

        self.listCaps = wx.ListCtrl(id = wxID_WXFRAME1LISTCAPS, name = 'listCaps', parent = self.splitterWindow1, pos = wx.Point(2, 2), size = wx.Size(756, 378), style=wx.LC_REPORT, validator = wx.DefaultValidator)
        self._init_coll_listCaps_Columns(self.listCaps)
        self.listCaps.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListcapsListItemSelected, id=wxID_WXFRAME1LISTCAPS)
        self.listCaps.Bind(wx.EVT_LEFT_DCLICK, self.OnListcapsLeftDclick)
        self.splitterWindow1.SplitHorizontally(self.listCaps, self.txtLog, 380)

        self.statusBar1 = wx.StatusBar(id = wxID_WXFRAME1STATUSBAR1, name = 'statusBar1', parent = self, style = 0)
        self._init_coll_statusBar1_Fields(self.statusBar1)
        self.SetStatusBar(self.statusBar1)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.prgInitialisation()

    def prgInitialisation(self):
        ### My Initialisation Code
        self.statusBar1.SetStatusText("", 0)
        self.statusBar1.SetStatusText("", 1)
        self.statusBar1.SetStatusText("1 - Pre-Session", 2)
        self.SM = None
        self.SS = None
        self.State = 0
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS1, False)
        self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS2, False)
        self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS3, False)


    def OnClose(self, event):
        if hasattr(self, "SS") and self.SS != None:
            self.SS.destroy()
            self.SS = None
        if hasattr(self, "SM") and self.SM != None:
            self.SM.destroy()
            self.SN = None
        self.Destroy()

    def Log(self, Message):
        ### Write a message to the log window
        self.txtLog.AppendText(Message)
        self.txtLog.AppendText("\n")
    def DisplayException(self, Title = None):
        ### Display the exception in a window
        txt = string.join(traceback.format_exception(
                sys.exc_type, sys.exc_value, sys.exc_traceback))
        dlg = wx.MessageDialog(self, txt,
                 Title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
    def OnFilemenuitems0Menu(self, event):
        ## Connect
        exceptionTitle=None
        try:
            if self.SS:
                exceptionTitle="Destroy Source Object"
                self.Log("del self.SS")
                self.Log("self.SS = None")
                del self.SS
                self.SS=None
                self.statusBar1.SetStatusText("3 - SourceManager Open", 2)
                self.statusBar1.SetStatusText("", 1)
            if not self.SM:
                exceptionTitle="Open SourceManager"
                self.statusBar1.SetStatusText("Attempting SourceManager Open", 0)
                self.Log("self.SM=twain.SourceManager(self.GetHandle())")
                self.SM = twain.SourceManager(self.GetHandle())
                self.Log("self.SM.SetCallback(self.OnTwainEvent)")
                self.SM.SetCallback(self.OnTwainEvent)
                if self.SM:
                    self.statusBar1.SetStatusText("3 - SourceManager Open", 2)

            exceptionTitle="Open Source"
            self.statusBar1.SetStatusText("Attempting Connect", 0)
            self.Log("self.SS=self.SM.OpenSource()")
            self.SS = self.SM.OpenSource()
            if self.SS:
                self.statusBar1.SetStatusText("4 - Source Open", 2)
                self.statusBar1.SetStatusText(self.SS.GetSourceName(), 1)
                ## Display the source information
                self.statusBar1.SetStatusText("Connected", 0)
                self.Log("self.SS.GetIdentity()")
                dlg = dlgIdentity.wxDialog1(self)
                dlg.SetSourceInfo(self, self.SS.GetIdentity())
                dlg.ShowModal()
                dlg.Destroy()
                self.OnFilemenuitems3Menu(event)
                self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS1, True)
                self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS2, True)
                self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS3, True)
            else:
                self.statusBar1.SetStatusText("Connect Cancelled", 0)
        except:
            self.DisplayException(exceptionTitle)

    def OnFilemenuitems1Menu(self, event):
        exceptionTitle=None
        try:
            if self.SS:
                self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS1, False)
                self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS2, False)
                self.FileMenu.Enable(wxID_WXFRAME1FILEMENUITEMS3, False)
                exceptionTitle="Destroy Source Object"
                self.Log("self.SS.destroy()")
                self.Log("self.SS = None")
                self.SS.destroy()
                self.SS=None
                self.listCaps.DeleteAllItems()
                self.LastSource = None
                self.statusBar1.SetStatusText("3 - SourceManager Open", 2)
                self.statusBar1.SetStatusText("", 1)
        except:
            self.DisplayException(exceptionTitle)


    def OnFilemenuitems2Menu(self, event):
        ## Acquire
        if not hasattr(self, "SS"): return
        Dlg = dlgAcquire.wxDialog1(self)
        Dlg.SetSourceInfo(self.SS, self)
        rv = Dlg.ShowModal()

    def OnFilemenuitems3Menu(self, event):
        ## Refresh Capabilities
        self.statusBar1.SetStatusText("Refreshing Capabilities", 0)
        if not hasattr(self, "CapabilityNames"):
            ## Get the list of names and store it
            capnames = filter(lambda x:len(x) > 3 and x[0:3] == "CAP",
                twain.__dict__.keys())
            capnames.sort()
            capnames1 = filter(lambda x:len(x) > 4 and x[0:4] == "ICAP",
                twain.__dict__.keys())
            capnames1.sort()
            capnames = capnames + capnames1
            capnames1 = filter(lambda x:len(x) > 4 and x[0:4] == "ACAP",
                twain.__dict__.keys())
            capnames1.sort()
            self.CapabilityNames = capnames + capnames1

            ## I use these for selecting the default value to set a capability.
            typenames = filter(lambda x:len(x) > 4 and x[0:4] == "TWTY",
                twain.__dict__.keys())
            self.typeIds = {}
            for name in typenames:
                self.typeIds[getattr(twain, name)] = name

        if not hasattr(self, "LastSource") or self.LastSource <> self.SS.GetSourceName():
            self.LastSource = self.SS.GetSourceName()
            self.listCaps.ClearAll()
            self._init_coll_listCaps_Columns(self.listCaps)
            listIndex = 0
            for capname in self.CapabilityNames:
                self.listCaps.InsertStringItem(listIndex, capname)
                listIndex = listIndex + 1

            ### Colour code the list, depending on whether the capability
            ### is in SUPPORTEDCAPS.
            (capType, supported_caps) = self.SS.GetCapability(twain.CAP_SUPPORTEDCAPS)
            for i in range(len(self.CapabilityNames)):
                capname = self.CapabilityNames[i]
                capId = getattr(twain, capname)
                item = self.listCaps.GetItem(i)
                if capId in supported_caps:
                    item.SetTextColour(wx.GREEN)
                else:
                    item.SetTextColour(wx.BLACK)
                self.listCaps.SetItem(item)

        ### Update the values
        for i in range(len(self.CapabilityNames)):
            capname = self.CapabilityNames[i]
            try:
                curval = ""
                capId = getattr(twain, capname)
                capInfo = self.SS.GetCapability(capId)
                if type(capInfo) == type({}):
                    capval = str(capInfo)   ## range
                else:
                    capval = str(capInfo[1])
                    (capType, curval) = self.SS.GetCapabilityCurrent(capId)
                try:
                    if type(curval) == type(0):
                        curval = "0x%x" % int(curval)
                    else:
                        curval = str(curval)
                except:
                    curval = str(curval)
            except:
                capval = str(sys.exc_type) + str(sys.exc_value)
            self.listCaps.SetStringItem(i, 1, capval)
            self.listCaps.SetStringItem(i, 2, curval)
        self.statusBar1.SetStatusText("Refreshed Capabilities", 0)

    def OnFilemenuitems4Menu(self, event):
        self.Close(1)

    def GetNameForType(self, TypeId):
        return self.typeIds[TypeId]

    def OnListcapsListItemSelected(self, event):
        self.currentItem = event.m_itemIndex

    def OnListcapsLeftDclick(self, event):
        if not hasattr(self, "SS"): return
        capName = self.listCaps.GetItemText(self.currentItem)
        capDlg = ChangeCap.wxDialog1(self)
        capDlg.SetSourceInfo(self.SS, self, capName)
        capDlg.ShowModal()
    def OnTwainEvent(self, event):
        self.Log("OnTwainEvent called, event=%d" % event)
        try:
            if event == twain.MSG_XFERREADY:
                self.Log('twain.MSG_XFERREADY event')
                self.statusBar1.SetStatusText("6 - Data Available", 2)
                self.statusBar1.SetStatusText("Transfering Data", 0)
                Dlg = dlgTransfer.wxDialog1(self)
                Dlg.SetSourceInfo(self.SS, self)
                Dlg.ShowModal()

                self.Log("self.SS.HideUI()")
                self.SS.HideUI()
            elif event == twain.MSG_CLOSEDSREQ:
                # Have to close the DS (note: not hide it)
                self.Log('twain.MSG_CLOSEDREQ event')
                self.OnFilemenuitems1Menu(None)
        except:
            self.DisplayException("OnTwainEvent")
    def LookUpConstant(self, prefix, value):
        ### This method is used to translate constants back into their
        ### logical names.
        self.InitialiseConstants()
        try:
            subset = self.Constants[prefix]
            return subset[value]
        except:
            return None
    def InitialiseConstants(self):
        if hasattr(self, "Constants"):
            return
        self.Constants = {}
        keys = twain.__dict__.keys()
        for k in keys:
            if k[0] != '_' and string.find(k, '_') != -1:
                prefix = string.split(k, '_', 1)[0]
                value = getattr(twain, k)
                if not self.Constants.has_key(prefix):
                    self.Constants[prefix] = {}
                self.Constants[prefix][value] = k
    def GetConstants(self, prefix):
        self.InitialiseConstants()
        return self.Constants[prefix]
