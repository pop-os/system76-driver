#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Main frontend

import os
import sys
import time
import gobject
import restore
import model
import system
import drivers
import ubuntuversion
import connection_test

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

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
SYS76LOGO_IMAGE = os.path.join(IMAGEDIR, 'logo.png')
SYS76SQUARE_LOGO = os.path.join(IMAGEDIR, 'logoSQUARE.png')
WINDOW_ICON = os.path.join(IMAGEDIR, '76icon.png')

class aboutDlg:
    """Shows the Unsupported dialog box"""

    def __init__(self, datadir):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'aboutDialog')

    def run(self):
        """Loads the unsupported Dialog"""
        self.dlg = self.wTree.get_widget("aboutDialog")
        self.square_logo = gtk.gdk.pixbuf_new_from_file(os.path.join(SYS76SQUARE_LOGO))
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_logo(self.square_logo)
        self.dlg.set_icon(self.icon)
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()
        
class connectDlg:
    """Shows no connection dialog"""
    
    def __init__(self, datadir):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'noConnection')
        
    def run(self):
        """Loads the no connection Dialog"""
        self.dlg = self.wTree.get_widget("noConnection")
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.dlg.set_icon(self.icon)
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()

def supported(datadir):
    """
    This function will determine System76 and Ubuntu
    Version support and run appropriate functions
    """
    modelname = model.determine_model()
    version = ubuntuversion.release()
    
    if version != '6.06' and version != '6.10' and version != '7.04' and version != '7.10':
        notsupported = unsupported(datadir);
        notsupported.run()
    elif modelname == ('nonsystem76'):
        notsupported = unsupported(datadir);
        notsupported.run()
    else:
        ui = System76Driver(datadir)
        ui.run()

class System76Driver:
    """This is the System76Driver application"""

    def __init__(self, datadir):
        
    #Set directory
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'mainWindow')

        #load logos
        self.system76logo = gtk.gdk.pixbuf_new_from_file(os.path.join(SYS76LOGO_IMAGE))
        self.wTree.get_widget('system76logo').set_from_pixbuf(self.system76logo)
        self.icon = gtk.gdk.pixbuf_new_from_file(os.path.join(WINDOW_ICON))
        self.wTree.get_widget('mainWindow').set_icon(self.icon)

        #Grab our widgets
        self.sysName = self.wTree.get_widget("sysName")
        self.sysModel = self.wTree.get_widget("sysModel")
        self.sysProcessor = self.wTree.get_widget("sysProcessor")
        self.sysMemory = self.wTree.get_widget("sysMemory")
        self.sysHardDrive = self.wTree.get_widget("sysHardDrive")

        #Create our dictionary and connect it
        dic = {"on_mainWindow_destroy" : gtk.main_quit
                , "on_about_clicked" : self.on_about_clicked
                , "on_close_clicked" : gtk.main_quit
                , "on_create_clicked" : self.on_create_clicked
                , "on_driverInstall_clicked" : self.on_driverInstall_clicked
                , "on_restore_clicked" : self.on_restore_clicked}
        self.wTree.signal_autoconnect(dic)
        
        #Grab the data
        modelname = model.determine_model()
        systemname = system.name()
        
        #Determine system processor
        b = os.popen('sudo dmidecode -s processor-version')
        try:
            system_processor = b.readline().strip()
        finally:
            b.close()
        processor = system_processor
        
        #Determine Total Memory
        c = os.popen('cat /proc/meminfo | grep MemTotal:')
        try:
            total_memory = c.readline().strip()
        finally:
            c.close()
        memory = int(total_memory[15:22])
        readable_memory = str(memory) + str(' kB')
        
        #Determine Hard Drive Size
        d = os.popen('cat /proc/partitions | grep 0')
        try:
            total_drive = d.readline().strip()
        finally:
            d.close()
        hard_drive = int(total_drive[9:19])
        readable_drive = str(hard_drive/1000000) + str(' GB')
        
        #Change the labels
        self.sysName.set_label(systemname)
        self.sysModel.set_label(modelname)
        self.sysProcessor.set_label(processor)
        self.sysMemory.set_label(readable_memory)
        self.sysHardDrive.set_label(readable_drive)
        
    def on_about_clicked(self, widget):
    
        #Calls aboutDlg class to display dialog
        aboutDialog = aboutDlg(datadir);
        aboutDialog.run()
        
    def on_create_clicked(self, widget):
        
        #Creates an archive of common support files and logs
        today = time.strftime('%Y%m%d_h%Hm%Ms%S')
        modelname = model.determine_model()
        
        """
        Get OS Description
        """
        v = os.popen('lsb_release -d')
        try:
            ubuntuversion = v.readline().strip()
            version = ubuntuversion.split("\t")
        finally:
            v.close()
        return version[-1].lower()
        release = version
        
        os.mkdir('/tmp/system_logs_%s' % today)
        TARGETDIR = '/tmp/system_logs_%s' % today
        
        fileObject = file('/tmp/system_logs_%s/systeminfo.txt' % today, 'wt')
        fileObject.write('System76 Model: %s\n' % modelname)
        fileObject.write('OS Version: %s\n' % release)
        fileObject.close()
        os.system('sudo dmidecode > %s/dmidecode' % TARGETDIR)
        os.system('lspci -vv > %s/lspci' % TARGETDIR)
        os.system('sudo lsusb -vv > %s/lsusb' % TARGETDIR)
        os.system('cp /etc/X11/xorg.conf %s/' % TARGETDIR)
        os.system('cp /etc/default/acpi-support %s/' % TARGETDIR)
        os.system('cp /var/log/daemon.log %s/' % TARGETDIR)
        os.system('cp /var/log/dmesg %s/' % TARGETDIR)
        os.system('cp /var/log/messages %s/' % TARGETDIR)
        os.system('cp /var/log/Xorg.0.log %s/' % TARGETDIR)
        
        ## NEED TO COMPLETE
        ## CREATE ZIP ARCHIVE
        ## COPY TO DESKTOP

    def on_driverInstall_clicked(self, widget):
        
        #Grab internet connection test
        connection = connection_test.connectivityCheck()
        
        #Calls drivers module when user clicks Driver Install button
        if connection == "connectionExists":
            drivers.start()
        elif connection == "noConnectionExists":
            notConnected = connectDlg(datadir);
            notConnected.run()

    def on_restore_clicked(self, widget):
        
        #Grab internet connection test
        connection = connection_test.connectivityCheck()
        
        #Calls restore module when user clicks Restore button
        if connection == "connectionExists":
            restore.start()
        elif connection == "noConnectionExists":
            notConnected = connectDlg(datadir);
            notConnected.run()

    def run(self):
        gtk.main()
        
class unsupported:
    """Shows the Unsupported dialog box"""

    def __init__(self, datadir):
        #setup the glade file
        self.datadir = datadir
        self.wTree = gtk.glade.XML(os.path.join(self.datadir, 'system76driver.glade'), 'unsupported')

    def run(self):
        """Loads the unsupported Dialog"""
        self.dlg = self.wTree.get_widget("unsupported")
        
        #run the dialog      
        self.dlg.run()
        
        #we are done with the dialog, destroy it
        self.dlg.destroy()

if __name__ == "__main__":
    datadir = os.path.join(os.path.dirname(__file__),'.')
    supported(datadir)