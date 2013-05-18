
import twain
import traceback, sys
import os, os.path

XferByFile='File'
XferNatively='Natively'

tmpfilename="tmp.bmp"
OverrideXferFileName = 'c:/twainxfer.jpg'

class CannotWriteTransferFile(Exception):
    pass
    

class TwainBase:
    """Simple Base Class for twain functionality. This class should
    work with all the windows librarys, i.e. wxPython, pyGTK and Tk.
    """

    SM=None                        # Source Manager
    SD=None                        # Data Source
    ProductName='SimpleTwainDemo'  # Name of this product
    XferMethod = XferNatively      # Transfer method currently in use
    AcquirePending = False         # Flag to indicate that there is an acquire pending
    mainWindow = None              # Window handle for the application window

    # Methods to be implemented by Sub-Class
    def LogMessage(self, message):
        print("****LogMessage:", message)

    def DisplayImage(self, ImageFileName):
        """Display the image from a file"""
        print("DisplayImage:", message)

    # End of required methods


    def Initialise(self):
        """Set up the variables used by this class"""
        (self.SD, self.SM) = (None, None)
        self.ProductName='SimpleTwainDemo'
        self.XferMethod = XferNatively
        self.AcquirePending = False
        self.mainWindow = None

    def Terminate(self):
        """Destroy the data source and source manager objects."""
        if self.SD: self.SD.destroy()
        if self.SM: self.SM.destroy()
        (self.SD, self.SM) = (None, None)

    def OpenScanner(self, mainWindow=None, ProductName=None, UseCallback=False):
        """Connect to the scanner"""
        if ProductName: self.ProductName = ProductName
        if mainWindow: self.mainWindow = mainWindow
        if not self.SM:
            self.SM = twain.SourceManager(self.mainWindow, ProductName=self.ProductName)
        if not self.SM:
            return
        if self.SD:
            self.SD.destroy()
            self.SD=None
        self.SD = self.SM.OpenSource()
        if self.SD:
            self.LogMessage(self.ProductName+': ' + self.SD.GetSourceName())

        if UseCallback:
            self.SM.SetCallback(self.OnTwainEvent)
    
    def _Acquire(self):
        """Begin the acquisition process. The actual acquisition will be notified by 
        either polling or a callback function."""
        if not self.SD:
            self.OpenScanner()
        if not self.SD: return
        try:
            self.SD.SetCapability(twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, 100.0) 
        except:
            pass
        if self.XferMethod == XferByFile:
            xfermech = twain.TWSX_FILE
        elif self.XferMethod == XferNatively:
            xfermech = twain.TWSX_NATIVE
        self.SD.SetCapability(twain.ICAP_XFERMECH, twain.TWTY_UINT16, xfermech)
        self.SD.RequestAcquire(0, 0)  # 1,1 to show scanner user interface
        self.AcquirePending=True
        self.LogMessage(self.ProductName + ':' + 'Waiting for Scanner')
        if hasattr(self.SD, 'ModalLoop'):
            self.SD.ModalLoop()

    def AcquireNatively(self):
        """Acquire Natively - this is a memory based transfer"""
        self.XferMethod = XferNatively
        return self._Acquire()

    def AcquireByFile(self):
        """Acquire by file"""
        self.XferMethod = XferByFile
        return self._Acquire()

    def PollForImage(self):
        """This is a polling mechanism. Get the image without relying on the callback."""
        if self.AcquirePending:
            try:
                Info = self.SD.GetImageInfo()
            except twain.excTWCC_SEQERROR:
                Info = None
            if Info:
                self.AcquirePending = False
                self.ProcessXFer()

    def ProcessXFer(self):
        """An image is ready at the scanner - fetch and display it"""
        more_to_come = False
        try:
            if self.XferMethod == XferNatively:
                XferFileName=tmpfilename
                (handle, more_to_come) = self.SD.XferImageNatively()
                twain.DIBToBMFile(handle, XferFileName)
                twain.GlobalHandleFree(handle)
                self.LogMessage(self.ProductName + ':' + 'Image acquired natively')
            else:
                try:
                    XferFileName='TWAIN.TMP' # Default
                    rv = self.SD.GetXferFileName()
                    if rv:
                        (XferFileName, type) = rv

                    # Verify that the transfer file can be produced. Security 
                    # configurations on windows can prevent it working.
                    try:
                        self.VerifyCanWrite(XferFileName)
                    except CannotWriteTransferFile:
                        self.SD.SetXferFileName(OverrideXferFileName)
                        XferFileName = OverrideXferFileName

                except:
                    # Functionality to influence file name is not implemented.
                    # The default is 'TWAIN.TMP'
                    pass

                self.VerifyCanWrite(XferFileName)
                self.SD.XferImageByFile()
                self.LogMessage(self.ProductName + ':' + "Image acquired by file (%s)" % XferFileName)

            self.DisplayImage(XferFileName)
            if more_to_come: self.AcquirePending = True
            else: self.SD = None
        except:
            # Display information about the exception
            import sys, traceback
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2])

    def OnTwainEvent(self, event):
        """This is an event handler for the twain event. It is called 
        by the thread that set up the callback in the first place.

        It is only reliable on wxPython. Otherwise use the Polling mechanism above.
        
        """
        try:
            if event == twain.MSG_XFERREADY:
                self.AcquirePending = False
                self.ProcessXFer()
            elif event == twain.MSG_CLOSEDSREQ:
                self.SD = None
        except:
            # Display information about the exception
            import sys, traceback
            ei = sys.exc_info()
            traceback.print_exception(ei[0], ei[1], ei[2])

    def VerifyCanWrite(self, filepath):
        """The scanner can have a configuration with a transfer file that cannot
        be created. This method raises an exception for this case."""
        parts = os.path.split(filepath)
        if parts[0]:
            dirpart=parts[0]
        else:
            dirpart='.'
        if not os.access(dirpart, os.W_OK):
            raise CannotWriteTransferFile(filepath)
        

