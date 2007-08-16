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
    Get Ubuntu Version. Can be 6.06 or 6.10 or 7.04
    """
    v = os.popen('lsb_release -r')
    try:
        ubuntuversion = v.readline().strip()
        version = ubuntuversion.split("\t")
    finally:
        v.close()
    return version[-1].lower()