#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## 
## Adds system76 driver repository

import os
import fileinput

def add():
    
    # Remove legacy repository listing in /etc/apt/sources.list
    
    for line in fileinput.input("/etc/apt/sources.list",inplace =1):
        line = line.strip()
        if not 'planet76.com' in line:
            print line
    
    # Add System76 software repository
    # Install System76 repo signing key and update sources
    
    os.system("sudo wget http://www.planet76.com/sources.list.d/system76.list -O /etc/apt/sources.list.d/system76.list")
    os.system("wget -q http://planet76.com/repositories/system76_dev.pub -O- | sudo apt-key add - && sudo apt-get update")
    
def xupdates():
       
    # Add Ubuntu x-updates PPA
    # Install Ubuntu x-updates PPA repo key
    
    os.system("sudo rm /etc/apt/sources.list.d/x-updates.list")
    os.system("echo deb http://ppa.launchpad.net/ubuntu-x-swat/x-updates/ubuntu `lsb_release -cs` main | sudo tee -a /etc/apt/sources.list.d/x-updates.list")
    os.system("echo deb-src http://ppa.launchpad.net/ubuntu-x-swat/x-updates/ubuntu `lsb_release -cs` main | sudo tee -a /etc/apt/sources.list.d/x-updates.list")
    os.system("sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B22AB97AF1CDFA9 && sudo apt-get update")