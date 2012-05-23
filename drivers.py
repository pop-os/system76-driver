#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Creates progress bar and installs drivers
## with driverscontrol.py module


import os
import sys
import time
import model
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
drivert1, drivert2 = 0, 0

#Setup Source Directory
datadir = os.path.join(os.path.dirname(__file__),'.')
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
WINDOW_ICON = os.path.join(IMAGEDIR, '76icon.svg')

class pulseSetter(threading.Thread):
    """This class sets the fraction of the progressbar"""
    
    # Set drivert2 to the PID for this thread
    global drivert2
    drivert2 = os.getpid()
    
    #Thread event, stops the thread if it is set.
    stopthread = threading.Event()
    
    def run(self):
        """Run method, this is the code that runs while thread is alive."""
        
        #Importing the progressbar widget from the global scope
        global driver_progress_bar 
        
        #While the stopthread event isn't setted, the thread keeps going on
        while not self.stopthread.isSet() :
            # Acquiring the gtk global mutex
            gtk.gdk.threads_enter()
            #Setting pulse
            driver_progress_bar.pulse()
            # Releasing the gtk global mutex
            gtk.gdk.threads_leave()
            #Delaying 100ms until the next iteration
            time.sleep(0.1)
            
    def stop(self):
        """Stop method, sets the event to terminate the thread's main loop"""
        self.stopthread.set()

class progressWindow:
    def __init__(self):
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'driverDialog')
    
    def run(self):
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("driverDialog")
        #Get the progress bar widget
        self.progress_bar = self.wTree.get_widget("driverProgress")
        #Set window logo
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_icon(self.icon)

        #Set Global Variables
        global driverDialog
        driverDialog = self.dlg
        
        global driver_progress_bar
        driver_progress_bar = self.progress_bar
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()

class driver(threading.Thread):
    """This class installs drivers for the system"""

    global driverDialog

    # Set drivert1 to the PID for this thread
    global drivert1
    drivert1 = os.getpid()

    #dps starts and stops the progress bar thread
    global dps
    #Thread event, stops the thread if it is set.
    stopthread = threading.Event()
    
    def run(self):
        """Thread installs drivers."""
        
        #While the stopthread event isn't set, the thread keeps going
        while not self.stopthread.isSet():
            driverscontrol.installDrivers()
            nodrivers = driverscontrol.nodrivers
            if nodrivers == "true":
                self.stopthread.set()
                dps.stop()
                driverDialog.destroy()
                needdrivers = noDrivers()
                needdrivers.run()
            else:
                dps.stop()
                self.stop()
            
    def stop(self):
        """Stop method, sets the event to terminate the thread's main loop"""
        self.stopthread.set()
        dps.stop()
        driverDialog.destroy()
        complete = driverComplete()
        complete.run()
        
class driverComplete:
    def __init__(self):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'driverComplete')
    
    def run(self):
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("driverComplete")

        #run the dialog
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()
        os.popen("kill -9 "+str(drivert1))
        os.popen("kill -9 "+str(drivert2))
        sys.exit(0)
        
class noDrivers:
    def __init__(self):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'noDrivers')
    
    def run(self):
        
        #Get the actual dialog widget
        self.dlg = self.wTree.get_widget("noDrivers")
        #Set window logo
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_icon(self.icon)

        #run the dialog
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()
        os.popen("kill -9 "+str(drivert1))
        os.popen("kill -9 "+str(drivert2))
        sys.exit(0)
       
def start():
    global dps
    dps = pulseSetter()
    dps.start()
    global dr
    dr = driver()
    dr.start()
    startdriver = progressWindow()
    startdriver.run()