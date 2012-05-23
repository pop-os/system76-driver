#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Updates UVC driver when a new kernel is installed
import os

WEBCAMDIR1 = os.path.join(os.path.dirname(__file__), 'uvcvideo-74ad936bcca2-custom')
WORKDIR = os.path.join(os.path.dirname(__file__), '.')

# Get the driver
os.chdir(WORKDIR)
os.system('sudo rm -r /opt/system76/system76-driver/src/uvcvideo-74ad936bcca2-custom/')
os.system('sudo rm /opt/system76/system76-driver/src/uvcvideo-74ad936bcca2-custom.tar.gz')
os.system("sudo wget http://planet76.com/webcam/uvcvideo-74ad936bcca2-custom.tar.gz")
os.system("tar -xf uvcvideo-74ad936bcca2-custom.tar.gz")
# Configure and Install Driver
os.chdir(WEBCAMDIR1)
os.system("sudo make && sudo make install")
os.system('sudo rm -r /opt/system76/system76-driver/src/uvcvideo-74ad936bcca2-custom/')
os.system('sudo rm /opt/system76/system76-driver/src/uvcvideo-74ad936bcca2-custom.tar.gz')