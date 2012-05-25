#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## 
## Install linux-backports-modules-hardy to fix the wireless
## LED on notebooks with Intel 3945/4965 cards

import os

class install():
    def install(self):
        
        os.system('sudo apt-get --assume-yes install linux-backports-modules-hardy')
        
    def describe(self):
        return "Wireless LED driver"
    