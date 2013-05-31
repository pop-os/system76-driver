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


CMDLINE_RE = re.compile('^GRUB_CMDLINE_LINUX_DEFAULT="(.*)"$')
CMDLINE_TEMPLATE = 'GRUB_CMDLINE_LINUX_DEFAULT="{}"'

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


WIFI_PM_DISABLE = """#!/bin/sh
# Installed by system76-driver
# Fixes poor Intel wireless performance when on battery power
/sbin/iwconfig wlan0 power off
"""

class wifi_pm_disable(EtcFileAction):
    relpath = ('pm', 'power.d', 'wireless')
    content = WIFI_PM_DISABLE
    mode = 0o755

    def describe(self):
        return _('Improve WiFi performance on Battery')


class lemu1(GrubAction):
    cmdline = 'quiet splash acpi_os_name=Linux acpi_osi='

    def describe(self):
        return _('Enable brightness hot keys')

