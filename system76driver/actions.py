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

from .mockable import SubProcess


CMDLINE_RE = re.compile('^GRUB_CMDLINE_LINUX_DEFAULT="(.*)"$')
CMDLINE_TEMPLATE = 'GRUB_CMDLINE_LINUX_DEFAULT="{}"'

WIFI_PM_DISABLE = """#!/bin/sh
# Installed by system76-driver
# Fixes poor Intel wireless performance when on battery power
/sbin/iwconfig wlan0 power off
"""


def random_tmp_filename(filename):
    random = b32encode(os.urandom(15)).decode('utf-8')
    return '.'.join([filename, random])


def add_ppa(ppa):
    SubProcess.check_call(['sudo', 'add-apt-repository', '-y', ppa])


def update():
    SubProcess.check_call(['sudo', 'apt-get', 'update'])


def install(*packages):
    assert packages
    cmd = ['sudo', 'apt-get', '-y', 'install']
    cmd.extend(packages)
    SubProcess.check_call(cmd)


class Action:
    def describe(self):
        """
        Return the user visible description of this action.

        Note: this string should be translatable.
        """
        name = self.__class__.__name__
        raise NotImplementedError(
            '{}.describe()'.format(name)
        )

    def isneeded(self):
        """
        Return `True` if this action is needed.

        For example, if specific configuration file fix has already been
        applied, this function should return `False`.
        """
        name = self.__class__.__name__
        raise NotImplementedError(
            '{}.isneeded()'.format(name)
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

    def isneeded(self):
        if self.read() != self.content:
            return True
        st = os.stat(self.filename)
        if stat.S_IMODE(st.st_mode) != self.mode:
            return True
        return False

    def perform(self):
        self.tmp = random_tmp_filename(self.filename)
        open(self.tmp, 'w').write(self.content)
        os.chmod(self.tmp, self.mode)
        os.rename(self.tmp, self.filename)


class EtcFileAction(Action):
    relpath = None
    content = None
    mode = 0o644

    def __init__(self, etcdir='/etc'):
        self.filename = path.join(etcdir, *self.relpath)

    def read(self):
        try:
            return open(self.filename, 'r').read()
        except FileNotFoundError:
            return None

    def isneeded(self):
        if self.read() != self.content:
            return True
        st = os.stat(self.filename)
        if stat.S_IMODE(st.st_mode) != self.mode:
            return True
        return False

    def perform(self):
        open(self.filename, 'w').write(self.content)
        os.chmod(self.filename, self.mode)


class GrubAction(Action):
    """
    Base class for actions that modify cmdline in /etc/default/grub.
    """

    cmdline = 'quiet splash'

    def __init__(self, etcdir='/etc'):
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
        for line in self.read().splitlines():
            match = CMDLINE_RE.match(line)
            if match:
                yield CMDLINE_TEMPLATE.format(self.cmdline)
            else:
                yield line

    def isneeded(self):
        return self.get_cmdline() != self.cmdline

    def perform(self):
        new = '\n'.join(self.iter_lines())
        open(self.filename, 'w').write(new)


class wifi_pm_disable(FileAction):
    relpath = ('etc', 'pm', 'power.d', 'wireless')
    content = WIFI_PM_DISABLE
    mode = 0o755

    def describe(self):
        return _('Improve WiFi performance on Battery')


class lemu1(GrubAction):
    cmdline = 'quiet splash acpi_os_name=Linux acpi_osi='

    def describe(self):
        return _('Enable brightness hot keys')


class fingerprintGUI(Action):
    def describe(self):
        return _('Fingerprint reader drivers and user interface')

    def isneeded(self):
        return True  # FIXME: Properly detect whether package is installed

    def perform(self):
        add_ppa('ppa:fingerprint/fingerprint-gui')
        update()
        install('fingerprint-gui', 'policykit-1-fingerprint-gui', 'libbsapi')


class plymouth1080(Action):
    value = 'GRUB_GFXPAYLOAD_LINUX="1920x1080"'

    def __init__(self, etcdir='/etc'):
        self.filename = path.join(etcdir, 'default', 'grub')

    def readlines(self):
        return open(self.filename, 'r').read().splitlines()

    def describe(self):
        return _('Correctly diplay Ubuntu logo on boot')

    def isneeded(self):
        return self.readlines()[-1] != self.value

    def iter_lines(self):
        for line in self.readlines():
            if not line.startswith('GRUB_GFXPAYLOAD_LINUX='):
                yield line
        yield self.value

    def perform(self):
        new = '\n'.join(self.iter_lines())
        open(self.filename, 'w').write(new)


class uvcquirks(FileAction):
    relpath = ('etc', 'modprobe.d', 'uvc.conf')
    content = 'options uvcvideo quirks=2'

    def describe(self):
        return _('Webcam quirk fixes')


class sata_alpm(EtcFileAction):
    relpath = ('pm', 'config.d', 'sata_alpm')
    content = 'SATA_ALPM_ENABLE=true'

    def describe(self):
        return _('Enable SATA Link Power Management (ALPM)')

