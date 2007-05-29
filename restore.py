#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Restores machine with base_system.py module

import os
import sys
import time
import model
import base_system
import driverscontrol
import gobject
import threading

try:
     import pygtk
     pygtk.require("2.0")
except:
      pass
try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

#Initializing the gtk's thread engine
gtk.gdk.threads_init()

#Keep track of thread PID's
restoret1, restoret2 = 0, 0

#Setup Source Directory
datadir = os.path.join(os.path.dirname(__file__),'.')
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
WINDOW_ICON = os.path.join(IMAGEDIR, '76icon.png')

class pulseSetter(threading.Thread):
    """This class sets the fraction of the progressbar"""
    
    # Set restoret2 to the PID for this thread
    global restoret2
    restoret2 = os.getpid()
    
    #Thread event, stops the thread if it is set.
    stopthread = threading.Event()
    
    def run(self):
        """Run method, this is the code that runs while thread is alive."""
        
        #Importing the progressbar widget from the global scope
        global progress_bar 
        
        #While the stopthread event isn't setted, the thread keeps going on
        while not self.stopthread.isSet() :
            # Acquiring the gtk global mutex
            gtk.gdk.threads_enter()
            #Setting pulse
            progress_bar.pulse()
            # Releasing the gtk global mutex
            gtk.gdk.threads_leave()
            #Delaying 100ms until the next iteration
            time.sleep(0.1)
            
    def stop(self):
        """Stop method, sets the event to terminate the thread's main loop"""
        self.stopthread.set()

class progressWindow:
    def __init__(self):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'restoreDialog')
    
    def run(self):
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("restoreDialog")
        #Get the progress bar widget
        self.progress_bar = self.wTree.get_widget("restoreProgress")
        #Set window logo
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_icon(self.icon)

        #Set Global Variables
        global restoreDialog
        restoreDialog = self.dlg
        
        global progress_bar
        progress_bar = self.progress_bar
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()

class restore(threading.Thread):
    """This class restores the system"""
    
    global restoreDialog

    # Set restoret1 to the PID for this thread
    global restoret1
    restoret1 = os.getpid()
    
    #ps starts and stops the progress bar thread
    global ps
    #Thread event, stops the thread if it is set.
    stopthread = threading.Event()
    
    def run(self):
        """Thread install base system."""
        
        #While the stopthread event isn't set, the thread keeps going
        while not self.stopthread.isSet():
            base_system.app_install()
            driverscontrol.installDrivers()
            ps.stop()
            self.stop()
            
    def stop(self):
        """Stop method, sets the event to terminate the thread's main loop"""
        self.stopthread.set()
        ps.stop()
        restoreDialog.destroy()
        complete = restoreComplete()
        complete.run()
        
class restoreComplete:
    def __init__(self):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'restoreComplete')
    
    def run(self):
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("restoreComplete")
        #Set window logo
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_icon(self.icon)

        #run the dialog
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()
        os.popen("kill -9 "+str(restoret1))
        os.popen("kill -9 "+str(restoret2))
        sys.exit(0)
       
def start():
    global ps
    ps = pulseSetter()
    ps.start()
    global r
    r = restore()
    r.start()
    startRestore = progressWindow()
    startRestore.run()