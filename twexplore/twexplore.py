#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import wxFrame1

modules ={'ChangeCap': [0, '', 'ChangeCap.py'],
 'dlgAcquire': [0, '', 'dlgAcquire.py'],
 'dlgFileXFer': [0, '', 'dlgFileXFer.py'],
 'dlgLayout': [0, '', 'dlgLayout.py'],
 'dlgTransfer': [0, '', 'dlgTransfer.py'],
 'frmViewBmp': [0, '', 'frmViewBmp.py'],
 'wxFrame1': [1, 'Main frame of Application', 'wxFrame1.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = wxFrame1.create(None)
        self.main.Show(True)
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
