#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
## Install gspca camera driver
import os

DRIVERDIR = os.path.join(os.path.dirname(__file__), 'gspcav1')

def camera():
    # Make and Install Driver
    os.chdir(DRIVERDIR)
    os.system("make")
    os.system("sudo make install")
