#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Hotkey setup for keys unsupported by Ubuntu vanilla

import os

def daru1_monitor_switch():
    # Copies required files
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/daru1/asus-display-switch /etc/acpi/events/asus-display-switch')
    os.system('sudo cp /opt/system76/system76-driver/src/acpi/daru1/asus-display-switch.sh /etc/acpi/asus-display-switch.sh')
    os.system('sudo chmod a+x /etc/acpi/asus-display-switch.sh')