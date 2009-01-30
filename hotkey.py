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
    
def daru1_touchpad_switch():
    # Enables SHMConfig for FN+F9 touchpad on/off switch
    marker="""<match key="info.product" contains="Synaptics TouchPad">"""
    newLine="""<merge key="input.x11_options.SHMConfig" type="string">On</merge>\n"""
    present = 0

    #Check for presence of newLine
    synapticsFile = open('/usr/share/hal/fdi/policy/20thirdparty/11-x11-synaptics.fdi','r')
    for line in synapticsFile:
        if line.strip() == newLine.strip():
            present = 1

    #Insert newLine if necessary
    synapticsFile.close()
    synapticsFile = open('/usr/share/hal/fdi/policy/20thirdparty/11-x11-synaptics.fdi','r')
    newFile = open('/opt/system76/newFile.txt','w')
    if present == 0:
        for line in synapticsFile:
            newFile.write(line)
            if line.strip() == marker.strip():
                newFile.write("        " + newLine)
        synapticsFile.close()
        newFile.close()
        command = "mv /opt/system76/newFile.txt /usr/share/hal/fdi/policy/20thirdparty/11-x11-synaptics.fdi"
        os.system(command)