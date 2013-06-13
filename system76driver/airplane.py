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
import fcntl
import sys

from .mockable import SubProcess


MASK1 = 0b01000000
MASK2 = 0b10111111


def log(msg):
    print('{:>8.2f}  {}'.format(time.monotonic(), msg))


def open_ec(sysdir='/sys'):
    SubProcess.check_call(['modprobe', 'ec_sys', 'write_support'])
    name = path.join(sysdir, 'kernel', 'debug', 'ec', 'ec0', 'io')
    fp = open(name, 'rb+')
    fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    return fp


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
        return clear_bit6(value)
    return set_bit6(value)


def read_state(state_file):
    key = open(state_file, 'r').read()
    return {'0\n': False, '1\n': True}[key] 


def write_state(state_file, value):
    assert isinstance(value, bool)
    open(state_file, 'w').write('{:d}\n'.format(value))


def iter_radios():
    rfkill = '/sys/class/rfkill'
    for radio in os.listdir(rfkill):
        key = open(path.join(rfkill, radio, 'name'), 'r').read().strip()
        state_file = path.join(rfkill, radio, 'state')
        yield (key, state_file)


def iter_state():
    for (key, state_file) in iter_radios():
        yield (key, read_state(state_file))


def iter_write_airplane_on():
    for (key, state_file) in iter_radios():
        write_state(state_file, False)
        yield (key, False)


def iter_write_airplane_off(restore):
    assert isinstance(restore, dict)
    log('restoring: {!r}'.format(restore))
    for (key, state_file) in iter_radios():
        value = restore.get(key, True)
        write_state(state_file, value)
        yield (key, value)


def sync_led(fd, airplane_mode):
    """
    Set LED state based on whether we are in *airplane_mode*.
    """
    old = read_int(fd, 0xD9)
    new = (set_bit6(old) if airplane_mode else clear_bit6(old))
    write_int(fd, 0xD9, new)


def run_loop():
    log('** process start **')
    old = None
    restore = {}
    fp = open_ec()
    fd = fp.fileno()
    while True:
        time.sleep(0.25)
        keypress = read_int(fd, 0xDB)
        new = dict(iter_state())
        if bit6_is_set(keypress):
            log('Fn+F11 keypress')
            airplane_mode = any(new.values())
            sync_led(fd, airplane_mode)
            if airplane_mode:
                restore = new
                old = dict(iter_write_airplane_on())
            else:
                old = dict(iter_write_airplane_off(restore))
            write_int(fd, 0xDB, clear_bit6(keypress))
            log('airplane_mode: {!r}\n'.format(airplane_mode))
        elif new != old:
            log('{!r} != {!r}'.format(new, old))
            old = new
            airplane_mode = not any(new.values())
            sync_led(fd, airplane_mode)
            log('airplane_mode: {!r}\n'.format(airplane_mode))
