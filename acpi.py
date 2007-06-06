#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Fixes Suspend and Hibernate on System76 machines
import os

def acpi1():
    """Configures S1 sleep"""
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/acpi-support /etc/default/acpi-support')
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/89-brightup.sh /etc/acpi/resume.d/89-brightup.sh')
    
def acpi2():
    """Configures S3 sleep"""
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/gazv3/acpi-support /etc/default/acpi-support')
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/feisty/89-brightup.sh /etc/acpi/resume.d/89-brightup.sh')