#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## What version of Ubuntu is running?

import os

def getVersion():
    """
    Get Ubuntu Version. Can be 6.06, 6.10, 7.04, 7.10, 8.04, 8.10,
    9.04, 9.10, 10.04, 10.10, 11.04, 11.10, 12.04, 12.10, 13.04
    """
    v = os.popen('lsb_release -r')
    try:
        ubuntuversion = v.readline().strip()
        version = ubuntuversion.split("\t")
    finally:
        v.close()
    return version[-1].lower()

def release():
    #Translate any odd version numbers into Ubuntu equivalents
    #NOTE: KEEP THESE EXCEPTIONS IN ALPHABETICAL ORDER!
    
    version = getVersion()
    if version == "0.2":
        version = "12.04"
    
    return version
    
def driver():
    #returns current System76 Driver version
    return "3.2.4"

def getOsName():
    #Find out the name of the OS we're running
    
    n = os.popen('lsb_release -i')
    try:
        distroname = n.readline().strip()
        name = distroname.split("\t")
    finally:
        n.close()
    return name[-1].capitalize()
