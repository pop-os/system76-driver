#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Common sound driver installation
import os
import urllib

WORKDIR = os.path.join(os.path.dirname(__file__), '.')
SOUNDDIR1 = os.path.join(os.path.dirname(__file__), 'sys76-alsa-1.0.14rc2')
SOUNDDIR2 = os.path.join(os.path.dirname(__file__), 'sys76-alsa-1.0.14rc3')
SOUNDDIR3 = os.path.join(os.path.dirname(__file__), 'sys76-alsa-1.0.14')

def alsa1():
    """Installs alsa 1.0.14rc2"""
    if os.path.exists(SOUNDDIR1) == True:
        # Install kernel headers
        os.system("sudo apt-get --assume-yes install linux-headers-`uname -r` build-essential")
        # Configure and Install Driver
        os.chdir(SOUNDDIR1)
        os.system("sudo sh configure --with-oss=yes --with-cards=hda-intel,usb-audio --with-kernel=/usr/src/linux-headers-`uname -r`/")
        os.system("sudo make && sudo make install")
        os.system("sudo make clean")
    elif os.path.exists(SOUNDDIR1) == False:
        # Get the driver
        os.chdir(WORKDIR)
        os.system("sudo wget http://planet76.com/sound/sys76-alsa-1.0.14rc2.tgz")
        os.system("tar -xzvf sys76-alsa-1.0.14rc2.tgz")
        # Install kernel headers
        os.system("sudo apt-get --assume-yes install linux-headers-`uname -r` build-essential")
        # Configure and Install Driver
        os.chdir(SOUNDDIR1)
        os.system("sudo sh configure --with-oss=yes --with-cards=hda-intel,usb-audio --with-kernel=/usr/src/linux-headers-`uname -r`/")
        os.system("sudo make && sudo make install")
        os.system("sudo make clean")
    else:
        raise OSError("A problem has occured.")
    
def alsa2():
    """Installs alsa 1.0.14rc3"""
    if os.path.exists(SOUNDDIR2) == True:
        # Install kernel headers
        os.system("sudo apt-get --assume-yes install linux-headers-`uname -r` build-essential")
        # Configure and Install Driver
        os.chdir(SOUNDDIR2)
        os.system("sudo sh configure --with-oss=yes --with-cards=hda-intel,usb-audio --with-kernel=/usr/src/linux-headers-`uname -r`/")
        os.system("sudo make && sudo make install")
        os.system("sudo make clean")
    elif os.path.exists(SOUNDDIR2) == False:
        # Get the Driver
        os.chdir(WORKDIR)
        os.system("sudo wget http://planet76.com/sound/sys76-alsa-1.0.14rc3.tar.gz")
        os.system("tar -xzvf sys76-alsa-1.0.14rc3.tar.gz")
        # Install kernel headers
        os.system("sudo apt-get --assume-yes install linux-headers-`uname -r` build-essential")
        # Configure and Install Driver
        os.chdir(SOUNDDIR2)
        os.system("sudo sh configure --with-oss=yes --with-cards=hda-intel,usb-audio --with-kernel=/usr/src/linux-headers-`uname -r`/")
        os.system("sudo make && sudo make install")
        os.system("sudo make clean")
    else:
        raise OSError("A problem has occured.")
    
def alsa3():
    """Installs alsa 1.0.14 final with realtek patches"""
    if os.path.exists(SOUNDDIR3) == True:
        # Install kernel headers
        os.system("sudo apt-get --assume-yes install linux-headers-`uname -r` build-essential")
        # Configure and Install Driver
        os.chdir(SOUNDDIR3)
        os.system("sudo sh configure --with-oss=yes --with-cards=hda-intel,usb-audio --with-kernel=/usr/src/linux-headers-`uname -r`/")
        os.system("sudo make && sudo make install")
        os.system("sudo make clean")
        os.system("echo options snd-hda-intel model=toshiba >> /etc/modprobe.d/alsa-base")
    elif os.path.exists(SOUNDDIR3) == False:
        # Get the Driver
        os.chdir(WORKDIR)
        os.system("sudo wget http://planet76.com/sound/sys76-alsa-1.0.14.tar.gz")
        os.system("tar -xzvf sys76-alsa-1.0.14.tar.gz")
        # Install kernel headers
        os.system("sudo apt-get --assume-yes install linux-headers-`uname -r` build-essential")
        # Configure and Install Driver
        os.chdir(SOUNDDIR3)
        os.system("sudo sh configure --with-oss=yes --with-cards=hda-intel,usb-audio --with-kernel=/usr/src/linux-headers-`uname -r`/")
        os.system("sudo make && sudo make install")
        os.system("sudo make clean")
        os.system("echo options snd-hda-intel model=toshiba >> /etc/modprobe.d/alsa-base")
    else:
        raise OSError("A problem has occured.")