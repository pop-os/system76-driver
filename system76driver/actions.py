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
import time
from base64 import b32encode
import datetime

import dbus

from . import get_datafile
from .model import get_edid_md5
from .mockable import SubProcess


CMDLINE_RE = re.compile('^GRUB_CMDLINE_LINUX_DEFAULT="(.*)"$')
CMDLINE_TEMPLATE = 'GRUB_CMDLINE_LINUX_DEFAULT="{}"'

WIFI_PM_DISABLE = """#!/bin/sh
# Installed by system76-driver
# Fixes poor Intel wireless performance when on battery power
/sbin/iwconfig wlan0 power off
"""


def random_id(numbytes=15):
    return b32encode(os.urandom(numbytes)).decode('utf-8')


def tmp_filename(filename):
    return '.'.join([filename, random_id()])


def backup_filename(filename, date=None):
    if date is None:
        date = datetime.date.today()
    return '.'.join([filename, 'system76-{}'.format(date)])


def add_apt_repository(ppa):
    SubProcess.check_call(['add-apt-repository', '-y', ppa])


def apt_get_update():
    SubProcess.check_call(['apt-get', 'update'])


def apt_get_install(*packages):
    assert packages
    cmd = ['apt-get', '-y', 'install']
    cmd.extend(packages)
    SubProcess.check_call(cmd)


def update_grub():
    SubProcess.check_call(['update-grub'])


def run_actions(actions, mocking=False):
    SubProcess.reset(mocking=mocking)
    for a in actions:
        if a.ppa:
            yield _('Adding {ppa}').format(ppa=a.ppa)
            add_apt_repository(a.ppa)

    if any(a.update_package_list for a in actions):
        yield _('Updating package list')
        apt_get_update()

    for cls in actions:
        inst = cls()
        yield inst.describe()
        if not mocking:
            inst.perform()

    if any(a.update_grub for a in actions):
        yield _('Running `update-grub`')
        update_grub()


class Action:
    ppa = None
    update_package_list = False
    update_grub = False

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

    def isneeded(self):
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


class lemu1(GrubAction):
    extra = ('acpi_os_name=Linux', 'acpi_osi=')

    def describe(self):
        return _('Enable brightness hot keys')


class backlight_vendor(GrubAction):
    """
    Added acpi_backlight=vendor to GRUB_CMDLINE_LINUX_DEFAULT (for gazp9).
    """

    extra = ('acpi_backlight=vendor',)

    def describe(self):
        return _('Enable brightness hot keys')


class airplane_mode(Action):
    update_package_list = True

    def describe(self):
        return _('Enable airplane-mode hot key')
 
    def isneeded(self):
        return True  # FIXME: Properly detect whether package is installed

    def perform(self):
        apt_get_install('system76-airplane-mode')


class fingerprintGUI(Action):
    ppa = 'ppa:fingerprint/fingerprint-gui'
    update_package_list = True

    def describe(self):
        return _('Fingerprint reader drivers and user interface')

    def isneeded(self):
        return True  # FIXME: Properly detect whether package is installed

    def perform(self):
        apt_get_install('fingerprint-gui', 'policykit-1-fingerprint-gui', 'libbsapi')


class plymouth1080(Action):
    update_grub = True
    value = 'GRUB_GFXPAYLOAD_LINUX="1920x1080"'

    def __init__(self, etcdir='/etc'):
        self.filename = path.join(etcdir, 'default', 'grub')

    def read(self):
        return open(self.filename, 'r').read()

    def describe(self):
        return _('Correctly diplay Ubuntu logo on boot')

    def isneeded(self):
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


# ICC Color Profiles:
NAME = 'org.freedesktop.ColorManager'
DEVICE = NAME + '.Device'
ICC = '/var/lib/colord/icc'


def get_object(obj, iface=None):
    proxy = dbus.SystemBus().get_object(NAME, obj)
    if iface:
        return dbus.Interface(proxy, dbus_interface=iface)
    return proxy


def get_prop(proxy, iface, key):
    return proxy.Get(iface, key,
        dbus_interface='org.freedesktop.DBus.Properties'
    )


def get_device(obj):
    return get_object(obj, DEVICE)


def get_profile_dst(name):
    return path.join(ICC, name)


def get_profile_obj(colord, filename):
    return colord.FindProfileByFilename(filename)




class ColorAction(Action):
    profiles = {}

    def describe(self):
        return _('ICC color profile for display')

    def isneeded(self):
        return True

    def atomic_write(self, icc, dst):
        self.tmp = path.join('/var/tmp', random_id())
        fp = open(self.tmp, 'xb')
        fp.write(icc)
        fp.flush()
        os.fsync(fp.fileno())
        os.rename(self.tmp, dst)

    def perform(self):
        edid = get_edid_md5()
        print('edid md5:', edid)
        if edid not in self.profiles:
            print('Warning: no profile available for this screen')
            return
        name = self.profiles[edid]
        src = get_datafile(name)
        dst = get_profile_dst(name)
        icc = open(src, 'rb').read()
        self.atomic_write(icc, dst)
        time.sleep(4)  # Give colord time to see the profile

        colord = get_object('/org/freedesktop/ColorManager', NAME)
        for device_obj in colord.GetDevicesByKind('display'):
            device = get_device(device_obj)
            model = get_prop(device, DEVICE, 'Model')
            print(device_obj, model)
            if model == 'Gazelle Professional':
                profile_obj = get_profile_obj(colord, dst)
                print('Profile:', profile_obj)
                try:
                    device.AddProfile('hard', profile_obj)
                except dbus.DBusException:
                    print('Warning: profile likely was already added to device')
                break


class gazp9_icc(ColorAction):
    profiles = {
        '38306ee6ae5ccf81d2951aa95ae823f4': 'system76-gazp9-glossy.icc',
        '6c4c6b27d0a90b99322e487510455230': 'system76-gazp9-ips-matte.icc',
    }
