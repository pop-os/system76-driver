#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Main frontend - GTK3 Version

#import system python libraries:
import os
import sys
import time
import threading

#import our python libraries
import model
import system
import ubuntuversion
import detect
import getpass
import base_system
import driverscontrol
import driversdescribe

#import GTK 3 libraries
from gi.repository import Gtk       
from gi.repository import GObject

GObject.threads_init() #initialize threads

lockFile = "/tmp/Sys76Lock.lock" #setup our lock file to prevent the driver from trying to do multiple things at once and...
os.system('rm ' + lockFile + ' 2>/dev/null') #...silently remove it if it exists for some reason
descriptionFile = "/tmp/sys76-drivers" #setup our description file that will hold descriptions of all of the drivers to be installed...
os.system("rm " + descriptionFile + " 2>/dev/null") #...and remove it too

#set some variables
programVersion = ubuntuversion.driver() #This sets the driver's version to be used throughout the application.
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
SYS76LOGO_IMAGE = os.path.join(IMAGEDIR, 'logo.png')
SYS76SQUARE_LOGO = os.path.join(IMAGEDIR, 'logoSQUARE.png')
WINDOW_ICON = os.path.join(IMAGEDIR, '76icon.svg')

def setNotify(icon, text): #Allows us to set the notification text and icon in the bottom of the window
    notifyIcon = builder.get_object("notifyImage")
    notifyText = builder.get_object("notifyLabel")
    notifyIcon.show()
    notifyText.show()
    notifyText.set_text(text)
    notifyIcon.set_from_stock(icon, 4)

#####################
## Create Log Dump ##
#####################
def onCreateClicked(driverCreate):
    #Creates an archive of common support files and logs    
    if os.path.isfile(lockFile) == True:
        print("FAIL: System76 Driver is currently locked! Wait for it to finish. If this error persists, please reboot.")
        setNotify("gtk-dialog-error", "The driver is currently processing another operation.\nPlease wait for it to finish")
    else:
        os.system('touch ' + lockFile)
        username = getpass.getuser()
        
        today = time.strftime('%Y%m%d_h%Hm%Ms%S')
        modelname = model.determine_model()
        version = ubuntuversion.release()
        
        os.mkdir('/tmp/system_logs_%s' % today)
        TARGETDIR = '/tmp/system_logs_%s' % today
        
        fileObject = file('/tmp/system_logs_%s/systeminfo.txt' % today, 'wt')
        fileObject.write('System76 Model: %s\n' % modelname)
        fileObject.write('OS Version: %s\n' % version)
        fileObject.close()
        os.system('sudo dmidecode > %s/dmidecode' % TARGETDIR)
        os.system('lspci -vv > %s/lspci' % TARGETDIR)
        os.system('sudo lsusb -vv > %s/lsusb' % TARGETDIR)
        os.system('cp /etc/X11/xorg.conf %s/' % TARGETDIR)
        os.system('cp /etc/default/acpi-support %s/' % TARGETDIR)
        os.system('cp /var/log/daemon.log %s/' % TARGETDIR)
        os.system('cp /var/log/dmesg %s/' % TARGETDIR)
        os.system('cp /var/log/messages %s/' % TARGETDIR)
        os.system('cp /var/log/syslog %s/' % TARGETDIR)
        os.system('cp /var/log/Xorg.0.log %s/' % TARGETDIR)
        os.system('tar -zcvf logs.tar %s/' % TARGETDIR)
        os.system('cp logs.tar /home/%s/' % username)
#        os.system('sudo chmod 777 /home/%s/logs.tar' % username)
        os.system('rm ' + lockFile)
        
        setNotify("gtk-ok", "A log file (logs.tar) was created in your home folder. Please send it to\nsupport via www.system76.com/support")

#########################
## Driver installation ##
#########################
class InstallThread(threading.Thread):
    #This thread is reponsible for installing the drivers.
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        GObject.idle_add(setNotify, "gtk-execute", "Now installing drivers. This may take a while...")
        time.sleep(0.1)
        if driverscontrol.installDrivers() == "true":
            GObject.idle_add(setNotify, "gtk-dialog-info", "All of the drivers for this system are provided by Ubuntu.")
            time.sleep(0.1)
            os.system('rm ' + lockFile)
        else:
            GObject.idle_add(setNotify, "gtk-apply", "Installation is complete! Reboot your machine for the changes to take effect.")
            time.sleep(0.1)
            os.system('rm ' + lockFile)

def onInstallClicked(driverInstall):
    #Manages installing the driver
    if os.path.isfile(lockFile) == True:
        print("FAIL: System76 Driver is currently locked! Wait for it to finish. If this error persists, please reboot.")
        setNotify("gtk-dialog-error", "The driver is currently processing another operation.\nPlease wait for it to finish")
    elif detect.connectivityCheck() == "noConnectionExists": #Check to ensure there's a connection
        print("FAIL: No internet connection, or connection to server down.")
        setNotify("gtk-dialog-warning", "You are not currently connected to the internet!\nPlease establish a wired or wireless internet connection.")
    elif detect.aptcheck() == "running": #Check if there's an APT process running.
        print("FAIL: Another APT process running. Please close it and retry or reboot")
        setNotify("gtk-dialog-warning", "A package manager is running! Please close it or\nreboot your system.")
    else:
        os.system('touch ' + lockFile)
        print("NOTE: Installing Drivers")
        installer = InstallThread()
        installer.start()

####################
## Restore System ##
####################
class RestoreThread(threading.Thread):
    #This thread is reponsible for installing the drivers.
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        GObject.idle_add(setNotify, "gtk-execute", "Now restoring factory settings. This may take a while...")
        time.sleep(0.1)
        base_system.app_install()
        driverscontrol.installDrivers()
        os.system('rm ' + lockFile)
        GObject.idle_add(setNotify, "gtk-apply", "System restore is complete! Reboot your machine for\nthe changes to take effect.")
        time.sleep(0.1)

def onRestoreClicked(driverRestore):
    #This method restores the system to factory state.
    if os.path.isfile(lockFile) == True:
        print("FAIL: System76 Driver is currently locked! Wait for it to finish. If this error persists, please reboot.")
        setNotify("gtk-dialog-error", "The driver is currently processing another operation.\nPlease wait for it to finish")
    elif detect.connectivityCheck() == "noConnectionExists": #Check to ensure there's a connection
        setNotify("gtk-dialog-warning", "You are not currently connected to the internet!\nPlease establish a wired or wireless internet connetion.")
    elif detect.aptcheck() == "running": #Check if there's an APT process running.
        setNotify("gtk-dialog-warning", "A package manager is running!\nPlease close it or reboot.")
    else:
        os.system('touch ' + lockFile)
        print("NOTE: Restoring system to factory state...")
        restorer = RestoreThread()
        restorer.start()

##################
## About Dialog ##
##################
def onAboutClicked(aboutButton):
    #displays the about dialog, and hides it when it's done
    print("NOTE: Showing about dialog")
    aboutDialog = builder.get_object("aboutDialog")
    aboutDialog.set_version(programVersion)
    aboutDialog.run() #open the dialog and...
    aboutDialog.hide() #...remove it when the user hits close
    
##################
## Details pane ##
##################
def onDetailsClicked(details):
    #figures out if we need to hide or show the details
    global DETAILS_SHOW
    detailsPane = builder.get_object("details_pane")
    detailsText = builder.get_object("detailsText")
    b = open(descriptionFile)
    d = b.read()
    b.close()
    detailsText.set_text(d)
    
    if DETAILS_SHOW == True:
        print("NOTE: Showing details of installed drivers")
        detailsPane.show()
        DETAILS_SHOW = False
    else:
        print("NOTE: Hiding details of installed drivers")
        detailsPane.hide()
        DETAILS_SHOW = True

builder = Gtk.Builder()
builder.add_from_file(os.path.join("system76Driver-gtk3.glade")) #initialize our glade file.

#create a dictionary for our commands and connect it
handlers = {
    "onDeleteWindow": Gtk.main_quit,
    "onInstallClicked": onInstallClicked,
    "onRestoreClicked": onRestoreClicked,
    "onCreateClicked": onCreateClicked,
    "onCloseClicked": Gtk.main_quit,
    "onAboutClicked": onAboutClicked,
}
builder.connect_signals(handlers)
    
def getSupported():
    #determine if the current system is fully supported by the driver
    version = ubuntuversion.release()
    modelname = model.determine_model()
    
    if version == ('8.04.1'): #because of a funky thing with 8.04
        version = '8.04'
    
    global supportStatus
    #check to make sure this is a System76 computer
    if modelname == ('nonsystem76'):
        supportStatus = "false"
    else:
        #Now, make sure it's running a supported OS and version. Includes Ubuntu 6.06 through 12.04 (unofficially, Elementary
        if version != '6.06' and version != '6.10' and version != '7.04' and version != '7.10' and version != '8.04' and version != '8.10' and version != '9.04' and version != '9.10' and version != '10.04' and version != '10.10' and version != '11.04' and version != '11.10' and version != '12.04' and version != '0.2':
            return False
        else:
            return True
    
    #get all of our GTK widgets
    modelName = builder.get_object("sysName")
    modelNumber = builder.get_object("sysModel")
    ubuntuVersion = builder.get_object("ubuntuVersion")
    driverVersion = builder.get_object("driverVersion")
    oSystem = builder.get_object("osVersionLabel")
    
    #set the strings and labels
    modelName.set_text(system.name())
    modelNumber.set_text(modelname)
    oSystem.set_text(ubuntuversion.getOsName())
    ubuntuVersion.set_text(ubuntuversion.getVersion())
    driverVersion.set_text(programVersion) 

class system76Driver(GObject.GObject):        
    #display the System76 Driver window
    
    def run(self, *args):
        #get all of our GTK widgets
        modelName = builder.get_object("sysName")
        modelNumber = builder.get_object("sysModel")
        ubuntuVersion = builder.get_object("ubuntuVersion")
        driverVersion = builder.get_object("driverVersion")
        oSystem = builder.get_object("osVersionLabel")
        
        #set the strings and labels
        modelName.set_text(system.name())
        modelNumber.set_text(model.determine_model())
        oSystem.set_text(ubuntuversion.getOsName() + " Version")
        ubuntuVersion.set_text(ubuntuversion.getVersion())
        driverVersion.set_text(programVersion)
        
        #set up the drivers details pane
        b = open(descriptionFile)
        d = b.read()
        b.close()
        builder.get_object("detailsText").set_text(d)
        
        #show the window.
        builder.get_object("mainWindow").show()
        Gtk.main()
        
class notSupport(object):
    #Display the unsupported window
    
    def run(self, *args):
        builder.get_object("unsupported").show()
        Gtk.main()

if getSupported() == True:
    if driversdescribe.describeDrivers() == "true":
        os.system("echo 'All of the drivers for this system are provided by Ubuntu.' > " + descriptionFile)
        os.system("cat " + descriptionFile)
    else:
        os.system("cat " + descriptionFile)
    system76Driver().run()
else:
    notSupport().run()

os.system('rm ' + lockFile + ' 2>/dev/null') #remove any stray lock files and...
os.system("rm " + descriptionFile + " 2>/dev/null") #description files.
sys.exit(0)
