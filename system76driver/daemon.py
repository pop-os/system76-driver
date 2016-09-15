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
User-space work-around for Airplane Mode hotkey (Fn+F11).

In the near future this will be replaced with a kernel driver to do the same.

ACPI virtual device for Fn+F11::

    Name (_HID, EisaId ("PNPC000"))
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
    'bonw9',
    'bonw10',
    'bonw11',
    'daru4',
    'galu1',
    'gazp9',
    'gazp9b',
    'gazp9c',
    'gaze10',
    'gaze11',
    'kudp1',
    'kudp1b',
    'kudp1c',
    'kudu2',
    'kudu3',
    'serw9',
    'serw10',
    'lemu6',
    'orxp1',
    'oryp2',
    'oryp2-dac',
])

# These products use 'acpi_video0' instead of 'intel_backlight':
NEEDS_BRIGHTNESS_ACPI = (
    'bonx7',
    'bonx8',
    'bonw9',
    'bonw10',
    'serw8-15',
    'serw8-17',
    'serw8-17g',
    'serw9',
    'orxp1',
)

# These products need software-base brightness restore:
NEEDS_BRIGHTNESS = NEEDS_BRIGHTNESS_ACPI + (
    'daru4',
    'galu1',
    'gazp9',
    'gazp9b',
    'gazp9c',
    'gaze10',
    'kudp1',
    'kudp1b',
    'kudp1c',
    'kudu2',
    'lemu5',
    'sabc1',
    'sabc2',
    'sabc3',
    'sabl4',
    'sabt1',
    'sabt2',
    'sabt3',
    'lemu6',
)


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
    fp = open(name, 'rb+', 0)
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
    return bool(int(open(state_file, 'rb', 0).read(11)))


def write_state(state_file, value):
    assert isinstance(value, bool)
    open(state_file, 'w').write('{:d}\n'.format(value))


def iter_radios(rfkill='/sys/class/rfkill'):
    for radio in os.listdir(rfkill):
        radio_dir = rfkill + '/' + radio
        key = open(radio_dir + '/name', 'rb', 0).read(20).strip().decode()
        yield (key, radio_dir + '/state')


def iter_state():
    for (key, state_file) in iter_radios():
        yield (key, bool(int(open(state_file, 'rb', 0).read(11))))


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
        self.fd = self.fp.fileno()
        self.sync_led_state = False
        self.old = None
        self.restore = {}

    def run(self):
        self.timeout_id = GLib.timeout_add(750, self.update)

    def update(self):
        try:
            self.sync_led_state ^= True
            keypress = os.pread(self.fd, 1, 0xDB)[0]
            if (keypress & 0b01000000):
                log.info('Fn+F11 keypress')
                new = dict(iter_state())
                airplane_mode = any(new.values())
                sync_led(self.fd, airplane_mode)
                if airplane_mode:
                    self.restore = new
                    self.old = dict(iter_write_airplane_on())
                else:
                    self.old = dict(iter_write_airplane_off(self.restore))
                write_int(self.fd, 0xDB, clear_bit6(keypress))
                log.info('airplane_mode: %r', airplane_mode)
            elif self.sync_led_state:
                new = dict(iter_state())
                if new != self.old:
                    log.info('%r != %r', new, self.old)
                    self.old = new
                    airplane_mode = not any(new.values())
                    sync_led(self.fd, airplane_mode)
                    log.info('airplane_mode: %r', airplane_mode)
            return True
        except Exception:
            log.exception('Error in AirplaneMode.update():')
            return False


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
    def __init__(self, model, name, rootdir='/'):
        assert name in ('intel_backlight', 'acpi_video0')
        self.model = model
        self.name = name
        self.key = '.'.join([model, name])
        self.current = None
        self.backlight_dir = path.join(rootdir, 
            'sys', 'class', 'backlight', name
        )
        self.max_brightness_file = path.join(self.backlight_dir, 'max_brightness')
        self.brightness_file = path.join(self.backlight_dir, 'brightness')
        self.saved_file = path.join(rootdir,
            'var', 'lib', 'system76-driver', 'brightness.json'
        )

    def read_max_brightness(self):
        with open(self.max_brightness_file, 'rb', 0) as fp:
            return int(fp.read(11))

    def read_brightness(self):
        with open(self.brightness_file, 'rb', 0) as fp:
            return int(fp.read(11))

    def write_brightness(self, brightness):
        assert isinstance(brightness, int) and brightness > 0
        with open(self.brightness_file, 'wb', 0) as fp:
            fp.write(str(brightness).encode())

    def load(self):
        conf = load_json_conf(self.saved_file)
        brightness = conf.get(self.key)
        if isinstance(brightness, int) and brightness > 0:
            return brightness
        try:
            max_brightness = self.read_max_brightness()
            log.info('max_brightness is %d', max_brightness)
            default = int(max_brightness * 0.75)
            if default > 0:
                log.info('will restore brightness to default of %d', default)
                return default
        except Exception:
            log.exception('Error reading %r', self.max_brightness_file)

    def save(self, brightness):
        assert isinstance(brightness, int)
        assert brightness > 0
        conf = load_json_conf(self.saved_file)
        conf[self.key] = brightness
        save_json_conf(self.saved_file, conf)

    def restore(self):
        current = self.load()
        assert current is None or (isinstance(current, int) and current > 0)
        if current is None:
            return
        log.info('restoring brightness to %d', current)
        if not path.exists(self.brightness_file):
            for i in range(10):
                log.warning('Waiting for %r', self.brightness_file)
                time.sleep(0.1)
                if path.exists(self.brightness_file):
                    break
        self.write_brightness(current)
        self.current = current

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
        brightness = self.read_brightness()
        if self.current != brightness:
            self.current = brightness
            if brightness > 0:
                log.info('saving brightness at %d', brightness)
                self.save(brightness)


def _run_brightness(model):
    if model not in NEEDS_BRIGHTNESS:
        log.info('Brightness hack not needed for %r', model)
        return
    log.info('Enabling brightness hack for %r', model)
    name = ('acpi_video0' if model in NEEDS_BRIGHTNESS_ACPI else 'intel_backlight')
    brightness = Brightness(model, name)
    brightness.restore()
    brightness.run()
    return brightness


def run_brightness(model):
    try:
        return _run_brightness(model)
    except Exception:
        log.exception('Error calling _run_brightness(%r):', model)

