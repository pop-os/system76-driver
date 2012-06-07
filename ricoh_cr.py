#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Install Ricoh Card Reader Driver

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

DRIVERDIR = os.path.join(os.path.dirname(__file__), 'ricoh')
descriptionFile = "/tmp/sys76-drivers"

class card_reader():
    def install(self):
        
        # Install Driver Package
        os.chdir(DRIVERDIR)
        os.system('sudo dpkg -i --force-architecture ricoh-r5c832-fix_1_i386.deb')
    
    def describe(self):
        os.system("echo 'Card reader driver' >> " + descriptionFile)
    