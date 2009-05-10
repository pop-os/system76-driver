#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Fixes Suspend and Hibernate on System76 machines
import os
import fileinput
import time

today = time.strftime('%Y%m%d_h%Hm%Ms%S')

def acpi1():
    """Configures S1 sleep"""
    os.system('sudo cp /etc/default/acpi-support /etc/default/acpi-support_sys76backup_%s' % today)
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/acpi-support /etc/default/acpi-support')
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/89-brightup.sh /etc/acpi/resume.d/89-brightup.sh')
    os.system('sudo cp /etc/acpi/resume.d/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh_sys76backup_%s' % today)
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh')
    
def acpi2():
    """Configures S3 sleep"""
    os.system('sudo cp /etc/default/acpi-support /etc/default/acpi-support_sys76backup_%s' % today)
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/gazv3/acpi-support /etc/default/acpi-support')
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/89-brightup.sh /etc/acpi/resume.d/89-brightup.sh')
    os.system('sudo cp /etc/acpi/resume.d/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh_sys76backup_%s' % today)
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh')
    
def acpi3():
    """Configures S1 sleep on Ubuntu 7.10"""
    os.system('sudo cp /etc/default/acpi-support /etc/default/acpi-support_sys76backup_%s' % today)
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/gutsy/acpi-support /etc/default/acpi-support')
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/89-brightup.sh /etc/acpi/resume.d/89-brightup.sh')
    os.system('sudo cp /etc/acpi/resume.d/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh_sys76backup_%s' % today)
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/60-asus-wireless-led.sh /etc/acpi/resume.d/60-asus-wireless-led.sh')

def acpi4():
    """Removes script used to temporarly fix Suspend with DRM on daru3
    Bug was fixed in Ubuntu"""
    os.system('sudo rm /etc/pm/sleep.d/00CPU')
    
def daru2():
    """Fix dsdt tables in daru2"""
    
    # Determine running kernel version
    b = os.popen('uname -r')
    try:
        uname = b.readline().strip()
    finally:
        b.close()
    kernel = uname
    
    os.system('sudo sh /opt/system76/system76-driver/src/acpi/initrd-add-dsdt.sh /boot/initrd.img-%s /opt/system76/system76-driver/src/acpi/daru2/DSDT.aml' % kernel)
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/daru2/DSDT.aml /etc/initramfs-tools/DSDT.aml')
    
    '''The ec_intr=0 option passes the embedded controller interupt
    to the kernel at boot.  On Ubuntu 7.10 the option fixes acpi
    battery notification problems.'''
    
    os.system('sudo cp /boot/grub/menu.lst /boot/grub/menu.lst_sys76backup_%s' % today)
    
    grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
    for line in grub_menu:
        print line.replace(' ec_intr=0',''),
    grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
    for line in grub_menu:
        print line.replace('splash','splash ec_intr=0'),
        
def osiNotWindows():
    # Kernel parameter tells the BIOS that the system is not Windows 2006
    
    os.system('sudo cp /boot/grub/menu.lst /boot/grub/menu.lst_sys76backup_%s' % today)
    
    grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
    for line in grub_menu:
        print line.replace(' acpi_osi="!Windows 2006"',''),
    grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
    for line in grub_menu:
        print line.replace('splash','splash acpi_osi="!Windows 2006"'),
        
def star1():
    
    # Fix wireless range issue  
    os.system('sudo apt-get --assume-yes install linux-backports-modules-jaunty')
    
    # Fix pciehp for SD card reader
    os.system('sudo cp /boot/grub/menu.lst /boot/grub/menu.lst_sys76backup_%s' % today)
    
    grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
    for line in grub_menu:
        print line.replace(' pciehp.pciehp_force=1',''),
    grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
    for line in grub_menu:
        print line.replace('splash','splash pciehp.pciehp_force=1'),