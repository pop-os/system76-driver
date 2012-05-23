#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Common sound driver installation
import os
import urllib
import model
import fileinput

WORKDIR = os.path.join(os.path.dirname(__file__), '.')
USRSRCDIR = os.path.join(os.path.dirname(__file__), '/usr/src/')
SOUNDDIR1 = os.path.join(os.path.dirname(__file__), 'sys76-alsa-1.0.14rc2')
SOUNDDIR2 = os.path.join(os.path.dirname(__file__), 'sys76-alsa-1.0.14rc3')
SOUNDDIR3 = os.path.join(os.path.dirname(__file__), 'sys76-alsa-1.0.14')
SOUNDDIR4 = os.path.join(os.path.dirname(__file__), 'alsa-driver')

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
    
    # Clean up /etc/modprobe.d/alsa-base file
    
    alsa_base = open("/etc/modprobe.d/alsa-base", "w")
    
    for line in fileinput.input("alsa_base",inplace =1):
        line = line.strip()
        if not 'toshiba' in line:
            print line
            
    for line in fileinput.input("alsa_base",inplace =1):
        line = line.strip()
        if not 'targa-dig' in line:
            print line
    
    """Installs alsa 1.0.14 final with realtek patches"""
    if os.path.exists(SOUNDDIR3) == True:
        # Install kernel headers
        os.system("sudo apt-get --assume-yes install linux-headers-`uname -r` build-essential")
        # Configure and Install Driver
        os.chdir(SOUNDDIR3)
        os.system("sudo sh configure --with-oss=yes --with-cards=hda-intel,usb-audio --with-kernel=/usr/src/linux-headers-`uname -r`/")
        os.system("sudo make && sudo make install")
        os.system("sudo make clean")
        os.system("echo options snd-hda-intel model=toshiba | sudo tee -a /etc/modprobe.d/alsa-base")
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
        os.system("echo options snd-hda-intel model=toshiba | sudo tee -a /etc/modprobe.d/alsa-base")
    
def alsa4():
    
    # Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not 'toshiba' in line:
            print line
            
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not 'targa-dig' in line:
            print line
            
    os.system("echo options snd-hda-intel model=targa-dig | sudo tee -a /etc/modprobe.d/alsa-base")

def alsa5():
    
    """Installs alsa 1.0.15rc3 source package.  Creates alsa-modules package.
    Installs alsa-modules package.  Replaces above alsa3 def.
    Adds "toshiba" line to alsa-base."""
    
    #Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not 'toshiba' in line:
            print line
            
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not 'targa-dig' in line:
            print line
    
    # Determine running kernel version
    b = os.popen('uname -r')
    try:
        uname = b.readline().strip()
    finally:
        b.close()
    kernel = uname
    
    # Check if alsa-modules-'uname -r' is installed
    b = os.popen('dpkg --get-selections | grep alsa-modules')
    try:
        installstatus = b.readline().strip()
        installed = installstatus.rstrip('install')
        version = installed.strip()
    finally:
        b.close()
        
    if version == "alsa-modules-%s" % kernel:
        alsa_installed = True
    else:
        alsa_installed = False
    
    # Change to the working directory
    os.chdir(WORKDIR)
    
    if alsa_installed == True:
        os.system("echo options snd-hda-intel model=toshiba | sudo tee -a /etc/modprobe.d/alsa-base")
        return
    elif os.path.isfile("alsa-source_1.0.15rc3-ldd1_all.deb") == True:
        os.system("sudo apt-get --assume-yes install build-essential debhelper intltool-debian po-debconf html2text debconf-utils module-assistant")
        os.system("sudo dpkg -i alsa-source_1.0.15rc3-ldd1_all.deb")
        os.chdir(USRSRCDIR)
        os.system("sudo module-assistant -t -i a-i alsa-source")
        os.system("echo options snd-hda-intel model=toshiba | sudo tee -a /etc/modprobe.d/alsa-base")
        return
    elif os.path.isfile("alsa-source_1.0.15rc3-ldd1_all.deb") == False:
        os.system("sudo wget http://planet76.com/sound/alsa-source_1.0.15rc3-ldd1_all.deb")
        os.system("sudo apt-get --assume-yes install build-essential debhelper intltool-debian po-debconf html2text debconf-utils module-assistant")
        os.system("sudo dpkg -i alsa-source_1.0.15rc3-ldd1_all.deb")
        os.chdir(USRSRCDIR)
        os.system("sudo module-assistant -t -i a-i alsa-source")
        os.system("echo options snd-hda-intel model=toshiba | sudo tee -a /etc/modprobe.d/alsa-base")
        return

def alsa6():
    
    """Installs alsa 1.0.15rc3 source package.  Creates alsa-modules package.
    Installs alsa-modules package.  Replaces above alsa1 and alsa2 defs."""
    
    # Determine running kernel version
    b = os.popen('uname -r')
    try:
        uname = b.readline().strip()
    finally:
        b.close()
    kernel = uname
    
    # Check if alsa-modules-'uname -r' is installed
    b = os.popen('dpkg --get-selections | grep alsa-modules')
    try:
        installstatus = b.readline().strip()
        installed = installstatus.rstrip('install')
        version = installed.strip()
    finally:
        b.close()
        
    if version == "alsa-modules-%s" % kernel:
        alsa_installed = True
    else:
        alsa_installed = False
    
    # Change to the working directory
    os.chdir(WORKDIR)
    
    if alsa_installed == True:
        return
    elif os.path.isfile("alsa-source_1.0.15rc3-ldd1_all.deb") == True:
        os.system("sudo apt-get --assume-yes install build-essential debhelper intltool-debian po-debconf html2text debconf-utils module-assistant")
        os.system("sudo dpkg -i alsa-source_1.0.15rc3-ldd1_all.deb")
        os.chdir(USRSRCDIR)
        os.system("sudo module-assistant -t -i a-i alsa-source")
        return
    elif os.path.isfile("alsa-source_1.0.15rc3-ldd1_all.deb") == False:
        os.system("sudo wget http://planet76.com/sound/alsa-source_1.0.15rc3-ldd1_all.deb")
        os.system("sudo apt-get --assume-yes install build-essential debhelper intltool-debian po-debconf html2text debconf-utils module-assistant")
        os.system("sudo dpkg -i alsa-source_1.0.15rc3-ldd1_all.deb")
        os.chdir(USRSRCDIR)
        os.system("sudo module-assistant -t -i a-i alsa-source")
        return
    
def alsa7():
    
    """Installs alsa 1.0.15rc3 source package.  Creates alsa-modules package.
    Installs alsa-modules package.  Adds "options snd-hda-intel model=6stack-dig" 
    line to alsa-base."""
    
    #Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not '6stack-dig' in line:
            print line
    
    # Determine running kernel version
    b = os.popen('uname -r')
    try:
        uname = b.readline().strip()
    finally:
        b.close()
    kernel = uname
    
    # Check if alsa-modules-'uname -r' is installed
    b = os.popen('dpkg --get-selections | grep alsa-modules')
    try:
        installstatus = b.readline().strip()
        installed = installstatus.rstrip('install')
        version = installed.strip()
    finally:
        b.close()
        
    if version == "alsa-modules-%s" % kernel:
        alsa_installed = True
    else:
        alsa_installed = False
    
    # Change to the working directory
    os.chdir(WORKDIR)
    
    if alsa_installed == True:
        os.system("echo options snd-hda-intel model=6stack-dig | sudo tee -a /etc/modprobe.d/alsa-base")
        return
    elif os.path.isfile("alsa-source_1.0.15rc3-ldd1_all.deb") == True:
        os.system("sudo apt-get --assume-yes install build-essential debhelper intltool-debian po-debconf html2text debconf-utils module-assistant")
        os.system("sudo dpkg -i alsa-source_1.0.15rc3-ldd1_all.deb")
        os.chdir(USRSRCDIR)
        os.system("sudo module-assistant -t -i a-i alsa-source")
        os.system("echo options snd-hda-intel model=6stack-dig | sudo tee -a /etc/modprobe.d/alsa-base")
        return
    elif os.path.isfile("alsa-source_1.0.15rc3-ldd1_all.deb") == False:
        os.system("sudo wget http://planet76.com/sound/alsa-source_1.0.15rc3-ldd1_all.deb")
        os.system("sudo apt-get --assume-yes install build-essential debhelper intltool-debian po-debconf html2text debconf-utils module-assistant")
        os.system("sudo dpkg -i alsa-source_1.0.15rc3-ldd1_all.deb")
        os.chdir(USRSRCDIR)
        os.system("sudo module-assistant -t -i a-i alsa-source")
        os.system("echo options snd-hda-intel model=6stack-dig | sudo tee -a /etc/modprobe.d/alsa-base")
        return

def alsa8():
    
    # Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not '6stack-dig' in line:
            print line
            
    os.system("echo options snd-hda-intel model=6stack-dig | sudo tee -a /etc/modprobe.d/alsa-base")
    
def alsa9():
    
    # Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not 'toshiba' in line:
            print line
            
    os.system("echo options snd-hda-intel model=toshiba | sudo tee -a /etc/modprobe.d/alsa-base")
    
def alsa10():
    
    # Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not '3stack-6ch-dig' in line:
            print line
            
    os.system("echo options snd-hda-intel model=3stack-6ch-dig | sudo tee -a /etc/modprobe.d/alsa-base")
    
def alsa11():
    
    # Install Alsa Driver 1.0.17 for mic and sound after resume support
    os.chdir(WORKDIR)
    os.system("sudo sh ./alsa-1.0.17.sh")
    
    # Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base",inplace =1):
        line = line.strip()
        if not '3stack-6ch-dig' in line:
            print line
            
    os.system("echo options snd-hda-intel model=3stack-6ch-dig | sudo tee -a /etc/modprobe.d/alsa-base")
    
def alsa12():
    
    # Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base.conf",inplace =1):
        line = line.strip()
        if not 'acer-aspire' in line:
            print line
            
    os.system("echo options snd-hda-intel model=acer-aspire | sudo tee -a /etc/modprobe.d/alsa-base.conf")
    os.system("gconftool-2 --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory --type string --set /system/gstreamer/0.10/default/audiosrc 'pulsesrc'")

def alsa13():
    
    # Clean up /etc/modprobe.d/alsa-base file
    
    for line in fileinput.input("/etc/modprobe.d/alsa-base.conf",inplace =1):
        line = line.strip()
        if not 'acer-aspire' in line:
            print line
            
    os.system("echo options snd-hda-intel model=acer-aspire | sudo tee -a /etc/modprobe.d/alsa-base.conf")
    
def alsabackportsLucid():
    
    # Install alsa backports
    os.system('sudo apt-get --assume-yes install linux-backports-modules-alsa-lucid-generic')
    
def audioDevPPA():
    """Install latest alsa release via Ubuntu Audio Dev PPA"""
    
    os.system("sudo add-apt-repository ppa:ubuntu-audio-dev/ppa")
    os.system("sudo apt-get update")
    os.system("sudo apt-get install linux-alsa-driver-modules-$(uname -r)")