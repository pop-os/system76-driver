#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Install uvc camera driver
import os

DRIVERDIR = os.path.join(os.path.dirname(__file__), 'uvc')
WEBCAMDIR1 = os.path.join(os.path.dirname(__file__), 'uvcvideo-74ad936bcca2-custom')
WORKDIR = os.path.join(os.path.dirname(__file__), '.')

def camera():
    # Make and Install Driver
    os.chdir(DRIVERDIR)
    os.system("sudo make")
    os.system("sudo make install")

def quirks():
    # adds quirks=2 when uvcvideo module loads
    os.system("sudo rm /etc/modprobe.d/uvc")
    os.system("sudo rm /etc/modprobe.d/uvc.conf")
    os.system("echo options uvcvideo quirks=2 | sudo tee -a /etc/modprobe.d/uvc.conf")

def lemu1():
    # compiles new UVC driver for Lemur Ultrathin webcam
    # remove any existing driver files
    os.system('sudo rm -r /opt/system76/system76-driver/src/uvcvideo-74ad936bcca2-custom/')
    os.system('sudo rm /opt/system76/system76-driver/src/uvcvideo-74ad936bcca2-custom.tar.gz')
    # Get the driver
    os.chdir(WORKDIR)
    os.system("sudo wget http://planet76.com/webcam/uvcvideo-74ad936bcca2-custom.tar.gz")
    os.system("tar -xf uvcvideo-74ad936bcca2-custom.tar.gz")
    # Install kernel headers
    os.system("sudo apt-get --assume-yes install linux-headers-`uname -r`")
    # Configure and Install Driver
    os.chdir(WEBCAMDIR1)
    os.system("sudo make && sudo make install")
    os.system("sudo rmmod uvcvideo")
    os.system("sudo modprobe uvcvideo")
    # remove driver files
    os.system('sudo rm -r /opt/system76/system76-driver/src/uvcvideo-74ad936bcca2-custom/')
    os.system('sudo rm /opt/system76/system76-driver/src/uvcvideo-74ad936bcca2-custom.tar.gz')
    os.chdir(WORKDIR)