#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## 
## Install linux-backports-modules-hardy to fix the wireless
## LED on notebooks with Intel 3945/4965 cards

## FORMATTING:
## Add new entries like this template:
"""
class exampleDriver():
    def install(self):
        ##Install example Driver
        {code to install goes here}
        {More code}
        
    def describe(self):
        os.system("echo 'Describe example driver here' >> " + descriptionFile)
"""

import os

descriptionFile = "/tmp/sys76-drivers"



class install():
    def install(self):
        
        os.system('sudo apt-get --assume-yes install linux-backports-modules-hardy')
        
    def describe(self):
        os.system("echo 'Wireless LED driver' >> " + descriptionFile)
    