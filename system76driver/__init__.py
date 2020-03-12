# system76-driver: Universal driver for System76 computers
# Copyright (C) 2005-2016 System76, Inc.
#
# This file is part of `system76-driver`.
#
# `system76-driver` is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# `system76-driver` is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with `system76-driver`; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
Universal driver for System76 computers
"""

from os import path
import logging


__version__ = '20.04.2'

datadir = path.join(path.dirname(path.abspath(__file__)), 'data')
log = logging.getLogger(__name__)


# Unfortunately, we need to accomidate some typos and goofs in sys_vendor:
VALID_SYS_VENDOR = (
    'System76',             # Current standard
    'System76, Inc.',       # Previous standard
    'System76, Inc',
    'System76, Inc .',
    'Notebook',
)


def get_datafile(name):
    return path.join(datadir, name)


def read_dmi_id(key, sysdir='/sys'):
    if key not in ('sys_vendor', 'product_version'):
        raise ValueError('bad dmi/id key: {!r}'.format(key))
    filename = path.join(sysdir, 'class', 'dmi', 'id', key)
    try:
        with open(filename, 'r') as fp:
            return fp.read(256).strip()
    except (FileNotFoundError, UnicodeDecodeError):
        pass


def get_sys_vendor(sysdir='/sys'):
    sys_vendor = read_dmi_id('sys_vendor', sysdir)
    if sys_vendor in VALID_SYS_VENDOR:
        return sys_vendor
    log.warning('invalid sys_vendor: %r', sys_vendor)


def get_product_version(sysdir='/sys'):
    if get_sys_vendor(sysdir) is not None:
        return read_dmi_id('product_version', sysdir)
