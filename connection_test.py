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

def connectivityCheck():
    """Throws error if no internet connection is available"""
    try:
        connectivityCheck = urllib2.urlopen('http://www.system76.com')
        return "connectionExists"
    except:
        return "noConnectionExists"
