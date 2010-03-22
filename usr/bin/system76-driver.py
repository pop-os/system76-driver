#!/usr/bin/env python
#
## System76, Inc.
## Universal Driver
## Copyright System76, Inc.
## Copyright (C) 2010 System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Startup script

import os
import sys

dir='/opt/system76/system76-driver/src/'

if os.path.isdir(dir):
    sys.path.append(dir)

import base_system
import driverscontrol
import optparse
import System76Driver

def main():
    
    parser = optparse.OptionParser(usage="%prog [options]", version="2.4.6")
    parser.add_option("-d", "--drivers", action="store_true", dest="drivers",
				help="Install Drivers for your Computer (requires sudo)")
    parser.add_option("-r", "--restore", action="store_true", dest="restore",
				help="Restore Computer to Factory Defaults (requires sudo)")

    (options, args) = parser.parse_args()

    if options.restore:
        base_system.app_install()
        driverscontrol.installDrivers()
    elif options.drivers:
        driverscontrol.installDrivers()
    else:
        try:
            os.environ['KDE_FULL_SESSION'] == 'true'
            os.system('kdesudo --comment "System76 Driver" python /opt/system76/system76-driver/src/System76Driver.py')
        except:
            os.environ['GDMSESSION'] == 'default'
            os.system('gksu --description /usr/share/applications/system76-driver.desktop python /opt/system76/system76-driver/src/System76Driver.py')
        else:
            os.system('gksu --description /usr/share/applications/system76-driver.desktop python /opt/system76/system76-driver/src/System76Driver.py')

if __name__ == "__main__":
    main()