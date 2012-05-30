#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Hotkey setup for keys unsupported by Ubuntu vanilla

import os
import fileinput

descriptionFile = "/tmp/sys76-drivers"

class daru1_monitor_switch():
    def install(self):
        
        # Copies required files
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/daru1/asus-display-switch /etc/acpi/events/asus-display-switch')
        os.system('sudo cp /opt/system76/system76-driver/src/acpi/daru1/asus-display-switch.sh /etc/acpi/asus-display-switch.sh')
        os.system('sudo chmod a+x /etc/acpi/asus-display-switch.sh')
        
    def describe(self):
        return "DarU1 monitor switch fix"
    
class daru1_touchpad_switch():
    def install(self):
        
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
            
    def describe(self):
        return "DarU1 touchpad hotkey fix"
        
class star1_904():
    def install(self):
        
        # Copy required files
        os.system('sudo cp /opt/system76/system76-driver/src/hotkeys/star1_904_30-keymap-system76.fdi /usr/share/hal/fdi/information/10freedesktop/30-keymap-system76.fdi')
        os.system('sudo cp /opt/system76/system76-driver/src/hotkeys/star1_904_wlonoff.sh /usr/local/bin/wlonoff.sh')
        os.system('sudo chmod a+x /usr/local/bin/wlonoff.sh')
        
        # Setup sudoers so user can turn on/off wireless without sudo
        for line in fileinput.input("/etc/sudoers",inplace =1):
            line = line.strip()
            if not 'WLTOGGLE' in line:
                print line
                
        os.system("echo Cmnd_Alias      WLTOGGLE=/usr/local/bin/wlonoff.sh | sudo tee -a /etc/sudoers")
        os.system("echo '%admin ALL=(ALL) NOPASSWD: WLTOGGLE' | sudo tee -a /etc/sudoers")
        
        # configure keybinding in gnome
        os.system("gconftool-2 --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory -s --type string /apps/metacity/keybinding_commands/command_2 'sudo /usr/local/bin/wlonoff.sh'")
        os.system("gconftool-2 --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory -s --type string /apps/metacity/global_keybindings/run_command_2 XF86WLAN")
        
    def describe(self):
        return "Star1 9.04 fix"