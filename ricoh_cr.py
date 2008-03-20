#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Install Ricoh Card Reader Driver
import os

DRIVERDIR = os.path.join(os.path.dirname(__file__), 'ricoh')

def card_reader():
    # Install Driver Package
    os.chdir(DRIVERDIR)
    os.system('sudo dpkg -i --force-architecture ricoh-r5c832-fix_1_i386.deb')