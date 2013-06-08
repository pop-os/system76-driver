# system76-driver: Universal driver for System76 computers
# Copyright (C) 2005-2013 System76, Inc.
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
User-space work-around for Airplane Mode hotkey (Fn+F11).
"""

import time
import os
from os import path

from .mockable import SubProcess

MASK1 = 0b01000000
MASK2 = 0b10111111


def open_ec(sysdir='/sys'):
    SubProcess.check_call(['modprobe', 'ec_sys', 'write_support'])
    name = path.join(sysdir, 'kernel', 'debug', 'ec', 'ec0', 'io')
    return open(name, 'rb+')


def read_int(fd, address):
    buf = os.pread(fd, 1, address)
    return buf[0]


def write_int(fd, address, value):
    assert isinstance(value, int)
    assert 0 <= value < 256
    buf = bytes([value])
    os.pwrite(fd, buf, address)


def bit6_is_set(value):
    return value & MASK1


def set_bit6(value):
    return value | MASK1


def clear_bit6(value):
    return value & MASK2


def toggle_bit6(value):
    if bit6_is_set(value):
        print('LED was on')
        return clear_bit6(value)
    print('LED was OFF')
    return set_bit6(value)


def iter_radios():
    rfkill = '/sys/class/rfkill'
    for name in os.listdir(rfkill):
        yield path.join(rfkill, name, 'state')


def run_loop():
    radios = tuple(iter_radios())
    fp = open_ec()
    fd = fp.fileno()
    while True:
        time.sleep(0.25)
        key = read_int(fd, 0xDB)
        if bit6_is_set(key):
            write_int(fd, 0xDB, clear_bit6(key))
            led = read_int(fd, 0xD9)
            state = (b'1' if bit6_is_set(led) else b'0')
            write_int(fd, 0xD9, toggle_bit6(led))
            for f in radios:
                open(f, 'wb').write(state)
