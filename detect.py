#!/usr/bin/env python
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## Written by Tom Aaron tom(at)system76(dot)com
##
## Test internet connection

import urllib2
import os

def aptcheck():
    """
    Check if any apt processes are running
    """
    p = os.popen("ps -U root -o comm")
    running = False
    pslist = p.readlines()
    p.close()
    for process in pslist:
        if process.strip() in ["dpkg", "apt-get","synaptic","update-manager", "adept", "adept-notifier"]:
            running = True
            break
    return "running"

def connectivityCheck():
    """Throws error if no internet connection is available"""
    try:
        connectivityCheck = urllib2.urlopen('http://www.system76.com')
        return "connectionExists"
    except:
        return "noConnectionExists"