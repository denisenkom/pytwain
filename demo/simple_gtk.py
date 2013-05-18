"""simple_gtk.py

This is a simple demonstration of the twain module using pyGTK.

This version does uses callbacks. Polling can be used instead by
modifying the global variable USE_CALLBACK below.

To use callbacks with pyGTK, you must use twainmodule 1.0.3 or later.
"""

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from simple_base import TwainBase

# You can either Poll the TWAIN source, or process the scanned image in an
# event callback. The event callback has not been fully tested using GTK.
# Specifically this does not work with Tkinter.
USE_CALLBACK=True


class ApplicationWindow(TwainBase):

    ui = '''<ui>
    <menubar name="MenuBar">
      <menu action="TWAIN">
        <menuitem action="Open Scanner"/>
        <menuitem action="Acquire By File"/>
        <menuitem action="Acquire Natively"/>
        <menuitem action="Quit"/>
      </menu>
    </menubar>
    </ui>'''


    def mnuOpenScanner(self, widget=None, event=None, data=None):
        """Connect to the scanner"""
        self.OpenScanner(self.window.window.handle,
            ProductName="Simple pyGTK Demo", UseCallback=USE_CALLBACK)
        return True
    
    def mnuAcquireNatively(self, widget=None, event=None, data=None):
        """Acquire Natively - this is a memory based transfer"""
        return self.AcquireNatively()

    def mnuAcquireByFile(self, widget=None, event=None, data=None):
        """Acquire by file"""
        return self.AcquireByFile()

    def onIdleTimer(self):
        """This is a polling mechanism. Get the image without relying on the callback."""
        self.PollForImage()
        return True

    def DisplayImage(self, ImageFileName):
        """Display the image from a file"""
        self.image.set_from_file(ImageFileName)
        self.image.show()

    def mnuQuit(self, widget=None, event=None, data=None):
        """I want an exit option on the menu. However, I don't know how to do it."""
        return gtk.main_quit()

    def LogMessage(self, title):
        """ Display the title in the window. I use this as a trivial
        trace of the current state of the program"""
        self.window.set_title(title)
        
    def OnQuit(self, event):
        gtk.main_quit()
        
    def __init__(self):
 
        """This is the pyGTK stuff to create the window and menubar"""
 
        # Set up Window
        window = self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(500, 500)
        window.connect("destroy", lambda w: gtk.main_quit())
        self.LogMessage("Twain Demo - pyGTK")
 
        # Set up Widget Container
        vbox = gtk.VBox(False, 0)
        window.add(vbox)
        vbox.show()
      
        # Setup the UI Manager for Menu    
        ui_manager = gtk.UIManager()
        
        # Add Accelerator Group
        accel_group = ui_manager.get_accel_group()
        window.add_accel_group(accel_group)
        
        # Add ActionGroup
        action_group = gtk.ActionGroup('Simple_GTK Actiongroup')
        
        # Create Actions
        action_group.add_actions(
            [
                 ("TWAIN",                None,    "TWAIN",                "<control>T",   None,    None),
                 ("Open Scanner",         None,    "Open Scanner",         "<control>O",   None,    self.mnuOpenScanner),
                 ("Acquire By File",      None,    "Acquire By File",      "<control>F",   None,    self.mnuAcquireByFile),
                 ("Acquire Natively",     None,    "Acquire Natively",     "<control>N",   None,    self.mnuAcquireNatively),
                 ("Quit",                 None,    "Quit",                 "<control>Q",   None,    self.OnQuit)
            ]
        )  
        
        # Attach the ActionGroup
        ui_manager.insert_action_group(action_group, 0)

        # Add a UI Description
        ui_manager.add_ui_from_string(self.ui)

        # Create a menu-bar to hold the menus and add it to our main window
        menubar = ui_manager.get_widget('/MenuBar')
        vbox.pack_start(menubar, False, False, 2)
        menubar.show()

        # Add an Image field to display what is scanned
        self.image = gtk.Image()
        vbox.pack_end(self.image, True, True, 2)
 
        # Display
        window.show()

        # Set up the idle timer. I use this to check to see if an image is ready.
        if not USE_CALLBACK:
            self.idleTimer = gobject.idle_add(self.onIdleTimer)
        

if __name__ == "__main__":
    app = ApplicationWindow()
    gtk.main()
