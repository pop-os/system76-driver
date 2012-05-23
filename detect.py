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
    pslist = p.readlines()
    p.close()
    for process in pslist:
        if process.strip() in ["dpkg", "apt-get","synaptic","update-manager", "adept", "adept-notifier"]:
            print("FAIL: You have APT running somewhere. Please close it or reboot.")
            return "running"
            break

def connectivityCheck():
    """Throws error if no internet connection is available"""
    try:
        connectivityCheck = urllib2.urlopen('http://www.system76.com')
        return "connectionExists"
    except:
        print("FAIL: No internet connection. Please connect first!")
        return "noConnectionExists"
    
def arch():
    """
    Detect whether the architecture is x86/ppc/amd64 
    """
    arch = os.uname()[-1]
    if arch in ('ppc', 'ppc64'):
        arch = 'powerpc'
    elif arch =='x86_64':
        arch = 'x86_64'
    elif arch in ('i386','i686','i586','k7'):
        arch = 'x86'
    return arch