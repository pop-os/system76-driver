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

import logging
from os import path
import subprocess
import time

from gi.repository import GLib


log = logging.getLogger(__name__)

# These products use 'acpi_video0' instead of 'intel_backlight':
NEEDS_BACKLIGHT = (
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

class Backlight:
    def __init__(self, model, name, rootdir='/'):
        assert name in ('acpi_video0')
        self.model = model
        self.name = name
        self.current = None
        self.backlight_dir = path.join(rootdir,
            'sys', 'class', 'backlight', name
        )
        self.max_brightness_file = path.join(self.backlight_dir, 'max_brightness')
        self.brightness_file = path.join(self.backlight_dir, 'brightness')
        self.xbacklight_max_brightness = 10

    def read_max_brightness(self):
        with open(self.max_brightness_file, 'rb', 0) as fp:
            return int(fp.read(11))

    def read_brightness(self):
        with open(self.brightness_file, 'rb', 0) as fp:
            return int(fp.read(11))

    def set_xbacklight(self, brightness):
        xbrightness = int(100 * brightness / self.xbacklight_max_brightness)
        if xbrightness == 0:
            xbrightness = 1
        if xbrightness <= 100:
            xbrightness_cmd = ['xbacklight',
                               '-set',
                               str(xbrightness)
            ]
            try:
                subprocess.check_output(xbrightness_cmd)
            except:
                time.sleep(1)

    def run(self):
        self.xbacklight_max_brightness = self.read_max_brightness()
        self.timeout_id = GLib.timeout_add(100, self.on_timeout)

    def on_timeout(self):
        try:
            self.update()
            return True
        except Exception:
            log.exception('Error calling Backlight.update():')
            return False

    def update(self):
        brightness = self.read_brightness()
        if self.current != brightness:
            self.current = brightness
            if brightness >= 0:
                self.set_xbacklight(brightness)
        return True

def _run_backlight(model):
    if model not in NEEDS_BACKLIGHT:
        log.info('Backlight hack not needed for %r', model)
        return
    log.info('Enabling backlight hack for %r', model)
    name = 'acpi_video0'
    backlight = Backlight(model, name)
    backlight.run()
    return backlight

def run_backlight(model):
    try:
        return _run_backlight(model)
    except Exception:
        log.exception('Error calling _run_brightness(%r):', model)
