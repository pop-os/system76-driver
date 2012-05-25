#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Installs fprint dependencies, libraries, and application
import os

DRIVERDIR = os.path.join(os.path.dirname(__file__), 'fprint')
LIBUSBDIR =  os.path.join(os.path.dirname(__file__), 'fprint/libusb-0.9.2')
LIBFPRINTDIR =  os.path.join(os.path.dirname(__file__), 'fprint/libfprint-20080810-6b8b17f5')
PAMFPRINTDIR = os.path.join(os.path.dirname(__file__), 'fprint/pam_fprint-20080330-5452ea09')
FPRINTDEMODIR = os.path.join(os.path.dirname(__file__), 'fprint/fprint_demo-20080319-5d86c3f7')
FPRINTGUI = os.path.join(os.path.dirname(__file__), 'fprint/fingerprint-0.12')


class install():
    def install(self):
        
        os.chdir(DRIVERDIR)
        # install dependencies
        os.system("sudo apt-get install --assume-yes build-essential libtool automake1.9 libssl-dev libgtk2.0-dev libmagick++9-dev libpam0g-dev")
        # untar the packages
        os.system("tar xjf libusb-0.9.2.tar.bz2")
        os.system("tar xjf libfprint-20080810-6b8b17f5.tar.bz2")
        os.system("tar xjf pam_fprint-20080330-5452ea09.tar.bz2")
        os.system("tar xjf fprint_demo-20080319-5d86c3f7.tar.bz2")
        # install libusb-1.0
        os.chdir(LIBUSBDIR)
        os.system("./configure --prefix=/usr")
        os.system("make")
        os.system("sudo make install")
        os.chdir(DRIVERDIR)
        # install libfprint
        os.chdir(LIBFPRINTDIR)
        os.system("sh autogen.sh")
        os.system("./configure --prefix=/usr")
        os.system("make")
        os.system("sudo make install")
        os.chdir(DRIVERDIR)
        # install pam_fprint
        os.chdir(PAMFPRINTDIR)
        os.system("cd pam_fprint-20080330-5452ea09/")
        os.system("sh autogen.sh")
        os.system("./configure --prefix=/usr")
        os.system("make")
        os.system("sudo make install")
        os.chdir(DRIVERDIR)
        # install fprint_demo
        os.chdir(FPRINTDEMODIR)
        os.system("sh autogen.sh")
        os.system("./configure --prefix=/usr")
        os.system("make")
        os.system("sudo make install")
        os.chdir(DRIVERDIR)
        # remove the directories
        os.system("sudo rm -r libusb-0.9.2/ libfprint-20080810-6b8b17f5/ pam_fprint-20080330-5452ea09/ fprint_demo-20080319-5d86c3f7/")
        # copy fprint menu item
        os.system("sudo cp fprint_demo.desktop /usr/share/applications/fprint_demo.desktop")
        
    def describe(self):
        return "Fingerprint Reader driver"
    
class installPackages():
    def isntall(self):
        
        os.system('sudo apt-get --assume-yes install libusb-1.0-0')
        os.chdir(DRIVERDIR)
        os.system('sudo dpkg -i libfprint0_20081125git-2_amd64.deb')
        os.system('sudo apt-get --assume-yes install fprint-demo libpam-fprint')
        # copy fprint menu item
        os.system("sudo cp fprint_demo.desktop /usr/share/applications/fprint-demo.desktop")
    
    def describe(self):
        return "Fingerprint Reader GUI packages"
    
class installUpek1():
    def install(self):
        
        os.system('sudo apt-get --assume-yes install libusb-1.0-0 libqca2-plugin-ossl libqtgui4 libfakekey0 libqt4-xml')
        os.chdir(DRIVERDIR)
        os.system('sudo dpkg -i libfprint0_20081125git-2_amd64.deb')
        os.system('sudo apt-get --assume-yes install libpam-fprint')
        # copy fprint menu item
        os.system('sudo cp z60_libfprint0.rules /etc/udev/rules.d/z60_libfprint0.rules')
        os.system('sudo chmod 644 /etc/udev/rules.d/z60_libfprint0.rules')
        os.system('wget http://planet76.com/fprint/fingerprintGUI-0.12.tar.gz')
        os.system('sudo tar zxf fingerprintGUI-0.12.tar.gz')
        os.chdir(FPRINTGUI)
        os.system('sudo sh install.sh --with-upek')
        os.chdir(DRIVERDIR)
        os.system('sudo rm -r fingerprint-0.12')
        os.system('sudo rm fingerprintGUI-0.12.tar.gz')
        
    def describe(self):
        return "Fingerprint reader driver"
    
class fingerprintGUI():
    def install(self):
        
        os.system('sudo add-apt-repository -y ppa:fingerprint/fingerprint-gui')
        os.system('sudo apt-get update')
        os.system('sudo apt-get install --assume-yes fingerprint-gui policykit-1-fingerprint-gui libbsapi')
        
    def describe(self):
        return "Fingerprint Reader GUI"