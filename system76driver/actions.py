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
Base class for system changes the driver can perform.
"""

from gettext import gettext as _
import os
from os import path
import stat
import re
from base64 import b32encode
import datetime
import logging

from . import get_datafile
from .mockable import SubProcess


log = logging.getLogger()
CMDLINE_RE = re.compile('^GRUB_CMDLINE_LINUX_DEFAULT="(.*)"$')
CMDLINE_TEMPLATE = 'GRUB_CMDLINE_LINUX_DEFAULT="{}"'

WIFI_PM_DISABLE = """#!/bin/sh
# Installed by system76-driver
# Fixes poor Intel wireless performance when on battery power
/sbin/iwconfig wlan0 power off
"""

HDMI_HOTPLUG_FIX = """#!/bin/sh
# Installed by system76-driver
# Turn off sound card power savings
# Fixes HDMI hotplug when on battery power
echo N > /sys/module/snd_hda_intel/parameters/power_save_controller
"""


def random_id(numbytes=15):
    return b32encode(os.urandom(numbytes)).decode('utf-8')


# FIXME: Should relocate these functions to a common file with just what's used
# by both `actions` and `daemon`.
def tmp_filename(filename):
    return '.'.join([filename, random_id()])


def backup_filename(filename, date=None):
    if date is None:
        date = datetime.date.today()
    return '.'.join([filename, 'system76-{}'.format(date)])


def update_grub():
    log.info('Calling `update-grub`...')
    SubProcess.check_call(['update-grub'])


class Action:
    _isneeded = None
    _description = None
    update_grub = False

    @property
    def isneeded(self):
        if self._isneeded is None:
            self._isneeded = self.get_isneeded()
        assert isinstance(self._isneeded, bool)
        return self._isneeded

    @property
    def description(self):
        if self._description is None:
            self._description = self.describe()
        assert isinstance(self._description, str)
        return self._description

    def describe(self):
        """
        Return the user visible description of this action.

        Note: this string should be translatable.
        """
        name = self.__class__.__name__
        raise NotImplementedError(
            '{}.describe()'.format(name)
        )

    def get_isneeded(self):
        """
        Return `True` if this action is needed.

        For example, if specific configuration file fix has already been
        applied, this function should return `False`.
        """
        name = self.__class__.__name__
        raise NotImplementedError(
            '{}.get_isneeded()'.format(name)
        )

    def perform(self):
        """
        Perform the action in question.

        This might modify a configuration file, install a package, etc.
        """
        name = self.__class__.__name__
        raise NotImplementedError(
            '{}.perform()'.format(name)
        )

    def atomic_write(self, content, mode=None):
        self.tmp = tmp_filename(self.filename)
        fp = open(self.tmp, 'x')
        fp.write(content)
        fp.flush()
        os.fsync(fp.fileno())
        if mode is not None:
            os.chmod(fp.fileno(), mode)
        os.rename(self.tmp, self.filename)

    def read_and_backup(self):
        content = self.read()
        self.bak = backup_filename(self.filename)
        try:
            open(self.bak, 'x').write(content)
        except FileExistsError:
            pass
        return content


class ActionRunner:
    def __init__(self, klasses):
        self.klasses = klasses
        self.actions = []
        self.needed = []
        for klass in klasses:
            assert issubclass(klass, Action)
            action = klass()
            self.actions.append(action)
            if action.isneeded:
                self.needed.append(action)

    def run_iter(self):
        for action in self.actions:
            name = action.__class__.__name__
            log.info('%s: %s', name, action.description)
            if action.isneeded:
                assert action in self.needed
                log.info('Running %r', name)
                yield action.description
                action.perform()
            else:
                assert action not in self.needed
                log.warning('Skipping %r as it was already applied', name)

        if any(action.update_grub for action in self.needed):
            yield _('Running `update-grub`')
            update_grub()


class FileAction(Action):
    relpath = tuple()
    content = ''
    mode = 0o644

    def __init__(self, rootdir='/'):
        self.filename = path.join(rootdir, *self.relpath)

    def read(self):
        try:
            return open(self.filename, 'r').read()
        except FileNotFoundError:
            return None

    def get_isneeded(self):
        if self.read() != self.content:
            return True
        st = os.stat(self.filename)
        if stat.S_IMODE(st.st_mode) != self.mode:
            return True
        return False

    def perform(self):
        self.atomic_write(self.content, self.mode)


class GrubAction(Action):
    """
    Base class for actions that modify cmdline in /etc/default/grub.
    """
    update_grub = True
    base = ('quiet', 'splash')
    extra = tuple()

    def __init__(self, etcdir='/etc'):
        params = self.base + self.extra
        self.cmdline = ' '.join(params)
        self.filename = path.join(etcdir, 'default', 'grub')

    def read(self):
        return open(self.filename, 'r').read()

    def get_cmdline(self):
        for line in self.read().splitlines():
            match = CMDLINE_RE.match(line)
            if match:
                return match.group(1)
        raise Exception('Could not parse GRUB_CMDLINE_LINUX_DEFAULT')

    def iter_lines(self):
        content = self.read_and_backup()
        for line in content.splitlines():
            match = CMDLINE_RE.match(line)
            if match:
                yield CMDLINE_TEMPLATE.format(self.cmdline)
            else:
                yield line

    def get_isneeded(self):
        return self.get_cmdline() != self.cmdline

    def perform(self):
        content = '\n'.join(self.iter_lines())
        self.atomic_write(content)


class wifi_pm_disable(FileAction):
    relpath = ('etc', 'pm', 'power.d', 'wireless')
    content = WIFI_PM_DISABLE
    mode = 0o755

    def describe(self):
        return _('Improve WiFi performance on Battery')


class hdmi_hotplug_fix(FileAction):
    relpath = ('etc', 'pm', 'power.d', 'audio')
    content = HDMI_HOTPLUG_FIX
    mode = 0o755

    def describe(self):
        return _('Fix HDMI hot-plugging when on battery')


class lemu1(GrubAction):
    extra = ('acpi_os_name=Linux', 'acpi_osi=')

    def describe(self):
        return _('Enable brightness hot keys')


class backlight_vendor(GrubAction):
    """
    Add acpi_backlight=vendor to GRUB_CMDLINE_LINUX_DEFAULT (for gazp9).
    """

    extra = ('acpi_backlight=vendor',)

    def describe(self):
        return _('Enable brightness hot keys')


class radeon_dpm(GrubAction):
    """
    Add radeon.dpm=1 to GRUB_CMDLINE_LINUX_DEFAULT (for panp7).
    """

    extra = ('radeon.dpm=1',)

    def describe(self):
        return _('Enable Radeon GPU power management')


class disable_power_well(GrubAction):
    """
    Add i915.disable_power_well=0 to GRUB_CMDLINE_LINUX_DEFAULT.

    This fixes the HDMI playback speed issue on Intel Haswell GPUs (playback
    speed is faster than it should be, aka the "chipmunk problem").
    """

    extra = ('i915.disable_power_well=0',)

    def describe(self):
        return _('Fix HDMI audio playback speed')


class grub_daru4(GrubAction):
    """
    Special daru4 action as GrubAction currently can't be merged.
    
    This has the effect of both `backlight_vendor` and `disable_power_well`.
    """

    extra = ('acpi_backlight=vendor', 'i915.disable_power_well=0',)

    def describe(self):
        return _('Fix brightness hot keys & HDMI audio playback speed')


class plymouth1080(Action):
    update_grub = True
    value = 'GRUB_GFXPAYLOAD_LINUX="1920x1080"'

    def __init__(self, etcdir='/etc'):
        self.filename = path.join(etcdir, 'default', 'grub')

    def read(self):
        return open(self.filename, 'r').read()

    def describe(self):
        return _('Correctly diplay Ubuntu logo on boot')

    def get_isneeded(self):
        return self.read().splitlines()[-1] != self.value

    def iter_lines(self):
        content = self.read_and_backup()
        for line in content.splitlines():
            if not line.startswith('GRUB_GFXPAYLOAD_LINUX='):
                yield line
        yield self.value

    def perform(self):
        content = '\n'.join(self.iter_lines())
        self.atomic_write(content)


class uvcquirks(FileAction):
    relpath = ('etc', 'modprobe.d', 'uvc.conf')
    content = 'options uvcvideo quirks=2'

    def describe(self):
        return _('Webcam quirk fixes')


class sata_alpm(FileAction):
    relpath = ('etc', 'pm', 'config.d', 'sata_alpm')
    content = 'SATA_ALPM_ENABLE=true'

    def describe(self):
        return _('Enable SATA Link Power Management (ALPM)')


class internal_mic_gain(FileAction):
    relpath = ('usr', 'share', 'pulseaudio', 'alsa-mixer', 'paths',
                    'analog-input-internal-mic.conf')

    _content = None

    @property
    def content(self):
        if self._content is None:
            fp = open(get_datafile('analog-input-internal-mic.conf'), 'r')
            self._content = fp.read()
        return self._content

    def describe(self):
        return _('Fix Internal Mic Gain')

