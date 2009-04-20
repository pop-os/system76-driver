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


def install():
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
