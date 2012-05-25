#!/usr/bin/env python
#
## System76, Inc.
## Universal Driver
## Copyright System76, Inc.
## Copyright (C) 2010 System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Startup script
#
#
##TODO: Remove debugging OS version string for final release!

import os
import sys

dir='/opt/system76/system76-driver/src/'

if os.path.isdir(dir):
    sys.path.append(dir)

import base_system
import driverscontrol
import optparse
import ubuntuversion

osversion = ubuntuversion.release()
driverversion = ubuntuversion.driver()
def main():
    
    parser = optparse.OptionParser(usage="%prog [options]", version=driverversion)
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
    
        if osversion != '6.06' and osversion != '6.10' and osversion != '7.04' and osversion != '7.10' and osversion != '8.04' and osversion != '8.10' and osversion != '9.04' and osversion != '9.10' and osversion != '10.04' and osversion != '10.10' and osversion != '11.04':
            try:
                print("NOTE: 11.10 or later detected! Running GTK3 version.")
                os.environ['KDE_FULL_SESSION'] == 'true'
                os.system('kdesudo --comment "System76 Driver" python /opt/system76/system76-driver/src/System76Drivergtk3.py')
            except:
                print("NOTE: 11.10 or later detected! Running GTK3 version.")
                os.environ['GDMSESSION'] == 'default'
                os.system('gksu --description /usr/share/applications/system76-driver.desktop python /opt/system76/system76-driver/src/System76Drivergtk3.py')
            else:
                print("NOTE: 11.10 or later detected! Running GTK3 version.")
                os.system('gksu --description /usr/share/applications/system76-driver.desktop python /opt/system76/system76-driver/src/System76Drivergtk3.py')
        else:
            try:
                print("NOTE: 11.04 or earlier detected! Running GTK2 version.")
                os.environ['KDE_FULL_SESSION'] == 'true'
                os.system('kdesudo --comment "System76 Driver" python /opt/system76/system76-driver/src/System76Driver.py')
            except:
                print("NOTE: 11.04 or earlier detected! Running GTK2 version.")
                os.environ['GDMSESSION'] == 'default'
                os.system('gksu --description /usr/share/applications/system76-driver.desktop python /opt/system76/system76-driver/src/System76Driver.py')
            else:
                print("NOTE: 11.04 or earlier detected! Running GTK2 version.")
                os.system('gksu --description /usr/share/applications/system76-driver.desktop python /opt/system76/system76-driver/src/System76Driver.py')

if __name__ == "__main__":
    main()

