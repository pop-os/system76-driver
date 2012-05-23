#!/bin/bash
#
## System76, Inc.
## Copyright System76, Inc.
## Released under the GNU General Public License (See LICENSE)
##
## This script inserts tifm card reader module names into /etc/modules

insert() {
    echo tifm_core >> /etc/modules
    echo tifm_sd >> /etc/modules
    echo tifm_7xx1 >> /etc/modules
    exit
}

insert
