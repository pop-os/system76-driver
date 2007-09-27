#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Fixes Suspend and Hibernate on System76 machines
import os
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
    
def dsdt_daru2():
    """Fix dsdt tables in daru2"""
    
    # Determine if dsdt patch has already been applied    
    a = os.popen('dmesg | grep "Looking for DSDT in initramfs"')
    try:
        dsdt = a.readline().strip()
    finally:
        a.close()
    dsdtstat = dsdt
    
    # Determin running kernel version
    b = os.popen('uname -r')
    try:
        uname = b.readline().strip()
    finally:
        b.close()
    kernel = uname
    
    if 'not found' in dsdtstat:
        os.system('sudo sh /opt/system76/system76-driver/src/acpi/initrd-add-dsdt.sh /boot/initrd.img-%s /opt/system76/system76-driver/src/acpi/daru2/dsdt.aml' % kernel)
    else:
        return