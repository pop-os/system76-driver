#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## What version of Ubuntu is running?

import os

def release():
    """
    Get Ubuntu Version. Can be 6.06, 6.10, 7.04, 7.10, 8.04, 8.10,
    9.04, or 9.10
    """
    v = os.popen('lsb_release -r')
    try:
        ubuntuversion = v.readline().strip()
        version = ubuntuversion.split("\t")
    finally:
        v.close()
    return version[-1].lower()
