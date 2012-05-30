#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Fix bugs or apply enhancements for usplash
import os
import fileinput
import time

today = time.strftime('%Y%m%d_h%Hm%Ms%S')
descriptionFile = "/tmp/sys76-drivers"

class gutsy_64_nvidia():
    def install(self):
        
        """Fix usplash on Ubuntu 7.10 64 bit nVidia based systems"""
        
        # Remove vesafb blacklist
        
        for line in fileinput.input("/etc/modprobe.d/blacklist-framebuffer",inplace =1):
            line = line.strip()
            if not 'vesafb' in line:
                print line
        
        # Remove existing xres and yres settings
        
        for line in fileinput.input("/etc/usplash.conf",inplace =1):
            line = line.strip()
            if not 'xres' in line:
                print line
        
        for line in fileinput.input("/etc/usplash.conf",inplace =1):
            line = line.strip()
            if not 'yres' in line:
                print line
        
        # Set usplash resolution
                
        os.system("echo xres=800 | sudo tee -a /etc/usplash.conf")
        os.system("echo yres=600 | sudo tee -a /etc/usplash.conf")
        
        # Remove lines so we don't duplicate
        
        for line in fileinput.input("/etc/usplash.conf",inplace =1):
            line = line.strip()
            if not 'fbcon' in line:
                print line
        
        for line in fileinput.input("/etc/usplash.conf",inplace =1):
            line = line.strip()
            if not 'vesafb' in line:
                print line
        
        # Add fbcon and vesafb modules to initramfs
        
        os.system("echo fbcon | sudo tee -a /etc/initramfs-tools/modules")
        os.system("echo vesafb | sudo tee -a /etc/initramfs-tools/modules")
        
        os.system("sudo update-initramfs -u")
        
        os.system('sudo cp /boot/grub/menu.lst /boot/grub/menu.lst_sys76backup_%s' % today)
        
        grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
        for line in grub_menu:
            print line.replace(' vga=789',''),
        grub_menu = fileinput.input('/boot/grub/menu.lst', inplace=1)
        for line in grub_menu:
            print line.replace('splash','splash vga=789'),
    
    def describe(self):
        return "USplash fix"