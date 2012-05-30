#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Installs Miscellaneous drivers

import os
import ubuntuversion
import jme_kernel_latest
import fileinput

WORKDIR = os.path.join(os.path.dirname(__file__), '.')
WIRELESS8187 = os.path.join(os.path.dirname(__file__), 'rtl8187B_linux_26.1052.0225.2009.release')
WIRELESS8187B = os.path.join(os.path.dirname(__file__), 'rtl8187B/rtl8187/')
JMEDIR = os.path.join(os.path.dirname(__file__), 'jme-1.0.5')
DKMSDIR = os.path.join(os.path.dirname(__file__), '/usr/src/')
descriptionFile = "/tmp/sys76-drivers"

class piix():
    def install(self):
        """Changes hard drive driver from ata_piix to piix"""
    
        a = os.popen('lsmod | grep ata_piix')
        try:
            ata_piix = a.readline().strip()
        finally:
            a.close()
        piix = ata_piix[0:8]
        
        if piix == "ata_piix":
            os.system("echo blacklist ata_piix | sudo tee -a /etc/modprobe.d/blacklist-ata")
            os.system("echo piix | sudo tee -a /etc/initramfs-tools/modules")
            os.system("sudo update-initramfs -u")
        else:
            return
        
    def describe(self):
        return "PIIX hard drive driver"
    
class piix2():
    def install(self):
        """Blacklist ata_piix and uses piix.  Required for the CDROM on
        Feisty Santa Rosa models.  Can render some models un-bootable.
        Test prior to applying to particular machines."""
    
        a = os.popen('lsmod | grep piix')
        try:
            ata_piix = a.readline().strip()
        finally:
            a.close()
        piix = ata_piix[0:4]
        
        if piix != "piix":
            os.system("echo blacklist ata_piix | sudo tee -a /etc/modprobe.d/blacklist-ata")
            os.system("echo piix | sudo tee -a /etc/initramfs-tools/modules")
            os.system("sudo update-initramfs -u")
        else:
            return
        
    def describe(self):
        return "PIIX hard drive driver"
        
class linux_backports():
    def install(self):
        """Install linux-backports-modules for the currently installed release"""
        
        os.system('sudo apt-get --assume-yes install linux-backports-modules-`lsb_release -c -s`')
    
    def describe(self):
        return "Linux-backports-modules"
    
class wireless8187b():
    
    def install(self):
        version = ubuntuversion.release()
        
        """Install updated 8187b wireless driver"""
        if version == ('9.04'):
            # blacklist old rtl8187 driver
            os.system("sudo rm /etc/modprobe.d/rtl8187.conf")
            os.system("echo blacklist rtl8187 | sudo tee -a /etc/modprobe.d/rtl8187.conf")
        
            if os.path.exists(WIRELESS8187) == True:
                # Install kernel headers
                os.system("sudo apt-get --assume-yes install linux-headers-`uname -r`")
                # Configure and Install Driver
                os.chdir(WIRELESS8187)
                os.system("sudo make && sudo make install")
            elif os.path.exists(WIRELESS8187) == False:
                # Get the driver
                os.chdir(WORKDIR)
                os.system("sudo wget http://drivers76.com/drivers/laptops/star1/rtl8187B_linux_26.1052.0225.2009.release.tar.gz")
                os.system("tar -xf rtl8187B_linux_26.1052.0225.2009.release.tar.gz")
                # Install kernel headers
                os.system("sudo apt-get --assume-yes install linux-headers-`uname -r`")
                # Configure and Install Driver
                os.chdir(WIRELESS8187)
                os.system("sudo make && sudo make install")
        elif version == ('9.10'):
            # blacklist old rtl8187 driver
            os.system("sudo rm /etc/modprobe.d/rtl8187.conf")
            os.system("echo blacklist rtl8187 | sudo tee -a /etc/modprobe.d/rtl8187.conf")
            
            # Place files to run driver install after new headers install
            os.system('sudo cp /opt/system76/system76-driver/src/rtl8187b /etc/kernel/header_postinst.d/rtl8187b')
            os.system('sudo chmod +x /etc/kernel/header_postinst.d/rtl8187b')
        
            # Get the driver
            os.chdir(WORKDIR)
            os.system("sudo wget http://planet76.com/drivers/star1/rtl8187B.tar.gz")
            os.system("tar -xf rtl8187B.tar.gz")
            # Configure and Install Driver
            os.chdir(WIRELESS8187B)
            os.system("sudo make && sudo make install")
            os.chdir(WORKDIR)
            os.system('sudo rm -r rtl8187B.tar.gz rtl8187B/')
        elif version == ('10.04'):
            # blacklist old rtl8187 driver
            os.system("sudo rm /etc/modprobe.d/rtl8187.conf")
            os.system("echo blacklist rtl8187 | sudo tee -a /etc/modprobe.d/rtl8187.conf")
            
            # Place files to run driver install after new headers install
            os.system('sudo cp /opt/system76/system76-driver/src/rtl8187b /etc/kernel/header_postinst.d/rtl8187b')
            os.system('sudo chmod +x /etc/kernel/header_postinst.d/rtl8187b')
            
            # Install dependencies
            os.system("sudo apt-get --assume-yes install build-essential")
            
            # Get the driver
            os.chdir(WORKDIR)
            os.system("sudo wget http://planet76.com/drivers/star1/rtl8187B.tar.gz")
            os.system("tar -xf rtl8187B.tar.gz")
            # Configure and Install Driver
            os.chdir(WIRELESS8187B)
            os.system("sudo make && sudo make install")
            os.chdir(WORKDIR)
            os.system('sudo rm -r rtl8187B.tar.gz rtl8187B/')
            
    def describe(self):
        return "RTL8187B Wireless Driver"
        
class jme_nic():
    def install(self):
        """Install 1.0.5 jme driver - fixes 4GB mem lag"""
        
        # Place files to run driver install after new headers install
        os.system('sudo cp /opt/system76/system76-driver/src/jme /etc/kernel/header_postinst.d/jme')
        os.system('sudo chmod +x /etc/kernel/header_postinst.d/jme')
        
        # Install the driver
        if os.path.exists(JMEDIR) == True:
            # Install Driver
            jme_kernel_latest.makefile_kernel()
            os.chdir(JMEDIR)
            os.system("sudo make install")
        elif os.path.exists(JMEDIR) == False:
            # Extract the driver
            os.chdir(WORKDIR)
            os.system('sudo tar xf /opt/system76/system76-driver/src/jme-1.0.5.tar.gz')
            # Install Driver
            jme_kernel_latest.makefile_kernel()
            os.chdir(JMEDIR)
            os.system("sudo make install")
            
    def describe(self):
        return "JME RAM driver 1.0.5"
        
class rm_aticatalyst():
    def install(self):
        """Remove Catalyst from the menu system (does not work well in Ubuntu 9.10)"""
        
        os.system('sudo rm /usr/share/applications/amdcccle.desktop /usr/share/applications/amdccclesu.desktop')
        
    def describe(self):
        return "Remove Catalyst Driver Control"
    
class gnomeThemeRace():
    def install(self):
        """On fast machines with nVidia graphics, a race condition causes the theme to not apply.
        A 2 second pause on gnome-settings start works around the bug"""
        
        gnome_settings = fileinput.input('/etc/xdg/autostart/gnome-settings-daemon.desktop', inplace=1)
        for line in gnome_settings:
            print line.replace('bash -c "sleep 2; /usr/lib/gnome-settings-daemon/gnome-settings-daemon"',''),
        gnome_settings = fileinput.input('/etc/xdg/autostart/gnome-settings-daemon.desktop', inplace=1)
        for line in gnome_settings:
            print line.replace('/usr/lib/gnome-settings-daemon/gnome-settings-daemon',''),
        gnome_settings = fileinput.input('/etc/xdg/autostart/gnome-settings-daemon.desktop', inplace=1)
        for line in gnome_settings:
            print line.replace('Exec=','Exec=bash -c "sleep 2; /usr/lib/gnome-settings-daemon/gnome-settings-daemon"'),
            
    def describe(self):
        return "Nvidia Driver Race Condition Fix"
        
class elantech():
    def install(self): 
        """Install elantech driver via DKMS. Used in natty on the panp8"""
        
        os.system('sudo apt-get --assume-yes install dkms')
        os.chdir(DKMSDIR)
        os.system('sudo wget http://planet76.com/drivers/elantech/psmouse-elantech-v6.tar.bz2')
        os.system('sudo tar jxvf psmouse-elantech-v6.tar.bz2')
        os.system('sudo dkms add -m psmouse -v elantech-v6')
        os.system('sudo dkms build -m psmouse -v elantech-v6')
        os.system('sudo dkms install -m psmouse -v elantech-v6')
        
    def describe(self):
        return "Elantech Touchpad Driver"

class realtek_rts_bpp():
    def install(self):
        """Install realtek rts_bpp driver via DKMS deb package. Driver unavailable in Ubuntu 12.04 and prior"""
    
        a = os.popen('lsmod | grep rts_bpp')
        try:
            rts_bpp = a.readline().strip()
        finally:
            a.close()
        realtek = rts_bpp[0:7]
        
        if realtek == "rts_bpp":
            os.system('sudo rm /lib/udev/rules.d/81-udisks-realtek.rules')
            os.system('echo \'DRIVERS=="rts_bpp", ENV{ID_DRIVE_FLASH_SD}="1"\' | sudo tee -a /lib/udev/rules.d/81-udisks-realtek.rules')
        else:
            os.system('sudo apt-get --assume-yes install dkms')
            os.chdir(DKMSDIR)
            os.system('sudo wget http://planet76.com/drivers/realtek/rts-bpp-dkms_1.1_all.deb')
            os.system('sudo dpkg -i rts-bpp-dkms_1.1_all.deb')
            os.system('sudo rm /lib/udev/rules.d/81-udisks-realtek.rules')
            os.system('echo \'DRIVERS=="rts_bpp", ENV{ID_DRIVE_FLASH_SD}="1"\' | sudo tee -a /lib/udev/rules.d/81-udisks-realtek.rules')
    def describe(self):
        return "Realtek Card Reader Driver"
    
class test():
    def install(self):
        #simple test method to see if the driver is working
        print("Installing drivers...")
        
    def describe(self):
        os.system("echo 'Test Driver 1' >> " + descriptionFile)
        return "Test Driver 1"

class test2():
    def install(self):
        print("Installing Test Driver 2")
        
    def describe(self):
        os.system("echo 'Test Driver 2' >> " + descriptionFile)
    
