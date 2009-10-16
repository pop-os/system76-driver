#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Common sound driver installation
import os

WORKDIR = os.path.join(os.path.dirname(__file__), '.')
WIRELESS8187 = os.path.join(os.path.dirname(__file__), 'rtl8187B_linux_26.1052.0225.2009.release')

def piix():
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
    
def piix2():
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
    
def linux_backports():
    """Install linux-backports-modules for the currently installed release"""
    
    os.system('sudo apt-get --assume-yes install linux-backports-modules-`lsb_release -c -s`')
    
def wireless8187b():
    """Install updated 8187b wireless driver"""

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
        os.system("tar -xzvf rtl8187B_linux_26.1052.0225.2009.release.tar.gz")
        # Install kernel headers
        os.system("sudo apt-get --assume-yes install linux-headers-`uname -r`")
        # Configure and Install Driver
        os.chdir(WIRELESS8187)
        os.system("sudo make && sudo make install")
    else:
        raise OSError("A problem has occured.")