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

In the near future this will be replaced with a kernel driver to do the same.
"""

import time
import os
from os import path
import logging
import json

from gi.repository import GLib

from .mockable import SubProcess


log = logging.getLogger(__name__)


# Two bit masks used for the Airplane Mode userspace driver:
MASK1 = 0b01000000
MASK2 = 0b10111111

# Products in this frozenset need the airplane mode hack
NEEDS_AIRPLANE = frozenset([
    'bonx7',
    'bonx8',
    'daru4',
    'galu1',
    'gazp9',
    'gazp9b',
    'kudp1',
    'kudp1b',
])

# Products in this dict need the brightness hack
DEFAULT_BRIGHTNESS = {
    'bonx7': ('acpi_video0', 64),
    'bonx8': ('acpi_video0', 6),
    'daru4': ('intel_backlight', 569),
    'galu1': ('acpi_video0', 70),
    'gazp9': ('intel_backlight', 690),
    'gazp9b': ('acpi_video0', 64),
    'kudp1': ('acpi_video0', 64),
    'kudp1b': ('acpi_video0', 64),
    'sabc1': ('acpi_video0', 82),
    'sabc2': ('acpi_video0', 82),
    'sabt1': ('acpi_video0', 82),
    'sabt2': ('acpi_video0', 82),
}


def get_model(sysdir='/sys'):
    name = path.join(sysdir, 'class', 'dmi', 'id', 'product_version')
    try:
        fp = open(name, 'r')
    except FileNotFoundError:
        return
    model = fp.read().strip()
    fp.close()
    return model


def load_json_conf(filename):
    try:
        fp = open(filename, 'r')
    except FileNotFoundError:
        return {}
    try:
        obj = json.load(fp)
    except Exception:
        log.exception('Error loading JSON conf from %r', filename)
        return {}
    if isinstance(obj, dict):
        return obj
    log.warning('does not contain JSON dict: %r', filename) 
    return {}


def save_json_conf(filename, obj):
    assert isinstance(obj, dict)
    tmp = filename + '.tmp'
    fp = open(tmp, 'w')
    json.dump(obj, fp, sort_keys=True, separators=(',',': '), indent=4)
    fp.flush()
    os.fsync(fp.fileno())
    os.rename(tmp, filename)
    fp.close()


def open_ec(sysdir='/sys'):
    SubProcess.check_call(['modprobe', 'ec_sys', 'write_support'])
    name = path.join(sysdir, 'kernel', 'debug', 'ec', 'ec0', 'io')
    fp = open(name, 'rb+')
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
    log.info('restoring: %r', restore)
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


class Airplane:
    def __init__(self):
        self.fp = open_ec()
        self.old = None
        self.restore = {}

    def run(self):
        self.timeout_id = GLib.timeout_add(500, self.on_timeout)

    def on_timeout(self):
        try:
            self.update()
            return True
        except Exception:
            log.exception('Error calling AirplaneMode.update():')
            return False

    def update(self):
        fd = self.fp.fileno()
        keypress = read_int(fd, 0xDB)
        new = dict(iter_state())
        if bit6_is_set(keypress):
            log.info('Fn+F11 keypress')
            airplane_mode = any(new.values())
            sync_led(fd, airplane_mode)
            if airplane_mode:
                self.restore = new
                self.old = dict(iter_write_airplane_on())
            else:
                self.old = dict(iter_write_airplane_off(self.restore))
            write_int(fd, 0xDB, clear_bit6(keypress))
            log.info('airplane_mode: %r', airplane_mode)
        elif new != self.old:
            log.info('%r != %r', new, self.old)
            self.old = new
            airplane_mode = not any(new.values())
            sync_led(fd, airplane_mode)
            log.info('airplane_mode: %r', airplane_mode)


def _run_airplane(model):
    if model not in NEEDS_AIRPLANE:
        log.info('Airplane mode hack not needed for %r', model)
        return
    log.info('Enabling airplane mode hack for %r', model)
    airplane_mode = Airplane()
    airplane_mode.run()
    return airplane_mode


def run_airplane(model):
    try:
        return _run_airplane(model)
    except Exception:
        log.exception('Error calling _run_airplane(%r):', model)


class Brightness:
    def __init__(self, model, name, default, rootdir='/'):
        assert isinstance(default, int)
        assert default > 0
        self.model = model
        self.name = name
        self.default = default
        self.current = None
        self.brightness_file = path.join(rootdir,
            'sys', 'class', 'backlight', name, 'brightness'
        )
        self.saved_file = path.join(rootdir,
            'var', 'lib', 'system76-driver', 'brightness.json'
        )

    def read(self):
        return int(open(self.brightness_file, 'r').read())

    def write(self, brightness):
        assert isinstance(brightness, int)
        assert brightness > 0
        open(self.brightness_file, 'w').write(str(brightness))

    def load(self):
        conf = load_json_conf(self.saved_file)
        brightness = conf.get(self.model)
        if isinstance(brightness, int) and brightness > 0:
            return brightness
        log.info('restoring with default brightness of %r', self.default)
        return self.default

    def save(self, brightness):
        assert isinstance(brightness, int)
        assert brightness > 0
        conf = load_json_conf(self.saved_file)
        conf[self.model] = brightness
        save_json_conf(self.saved_file, conf)

    def restore(self):
        self.current = self.load()
        log.info('restoring brightness to %d', self.current)
        if not path.exists(self.brightness_file):
            for i in range(10):
                log.warning('Waiting for %r', self.brightness_file)
                time.sleep(0.1)
                if path.exists(self.brightness_file):
                    break
        self.write(self.current)

    def run(self):
        self.timeout_id = GLib.timeout_add(10 * 1000, self.on_timeout)

    def on_timeout(self):
        try:
            self.update()
            return True
        except Exception:
            log.exception('Error calling Brightness.update():')
            return False

    def update(self):
        brightness = self.read()
        if self.current != brightness:
            self.current = brightness
            if brightness > 0:
                log.info('saving brightness at %d', brightness)
                self.save(brightness)


def _run_brightness(model):
    if model not in DEFAULT_BRIGHTNESS:
        log.info('Brightness hack not needed for %r', model)
        return
    log.info('Enabling brightness hack for %r', model)
    (name, default) = DEFAULT_BRIGHTNESS[model]
    brightness = Brightness(model, name, default)
    brightness.restore()
    brightness.run()
    return brightness


def run_brightness(model):
    try:
        return _run_brightness(model)
    except Exception:
        log.exception('Error calling _run_brightness(%r):', model)

