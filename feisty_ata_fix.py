#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Common sound driver installation
import os

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