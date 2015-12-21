# system76-driver: Universal driver for System76 computers
# Copyright (C) 2005-2015 System76, Inc.
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


__version__ = '15.10.11'

datadir = path.join(path.dirname(path.abspath(__file__)), 'data')


def get_datafile(name):
    return path.join(datadir, name)


def read_dmi_id(key, sysdir='/sys'):
    assert key in ('sys_vendor', 'product_version')
    filename = path.join(sysdir, 'class', 'dmi', 'id', key)
    try:
        fp = open(filename, 'r')
    except FileNotFoundError:
        return None
    try:
        value = fp.read(256).strip()
    except UnicodeDecodeError:
        value = None
    fp.close()
    return value

