#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Install Texeas Instruments tifm_7xx1 Card Reader Driver
import os

DRIVERDIR = os.path.join(os.path.dirname(__file__), 'tifm')

def card_reader():
    # Make and Install Driver
    os.chdir(DRIVERDIR)
    os.system("make")
    os.system("sudo cp -r /opt/system76/system76-driver/src/tifm /lib/modules/`uname -r`/")
    # Modprobe the drivers for immediate access
    os.system("sudo depmod")
    os.system("sudo modprobe tifm_core && sudo modprobe tifm_sd && sudo modprobe tifm_7xx1")
    # Shell script echos modules into /etc/modules
    # FIXME: Not sure if this is working yet, requires testing
    a = os.popen('grep tifm_core /etc/modules')
    try:
        mod = a.readline().strip()
    finally:
        a.close()
    modsin = mod
    if modsin != "tifm_core":
        os.system('sudo sh /opt/system76/system76-driver/src/tifm_modules.sh')
    else:
        return 0
