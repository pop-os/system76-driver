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
Base class for system changes the driver can perform.
"""

from gettext import gettext as _
import os
from os import path
import stat
import re
import json
from base64 import b32encode
import datetime
import logging

from . import get_datafile
from .mockable import SubProcess


log = logging.getLogger()
CMDLINE_RE = re.compile('^GRUB_CMDLINE_LINUX_DEFAULT="(.*)"$')
CMDLINE_TEMPLATE = 'GRUB_CMDLINE_LINUX_DEFAULT="{}"'
 
CMDLINE_CHECK_DEFAULT_RE = re.compile('^GRUB_CMDLINE_LINUX_DEFAULT')
CMDLINE_ADD_DEFAULT_RE = re.compile('^GRUB_CMDLINE_LINUX="(.*)"$')

LSPCI_RE = re.compile('^(.+) \[(.+)\]$')

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

DISABLE_PM_ASYNC = """# /etc/tmpfiles.d/system76-disable-pm_async.conf
w /sys/power/pm_async - - - - 0
"""


def random_id(numbytes=15):
    return b32encode(os.urandom(numbytes)).decode('utf-8')


# FIXME: Should relocate these functions to a common file with just what's used
# by both `actions` and `daemon`.
def tmp_filename(filename):
    return '.'.join([filename, random_id()])


def atomic_write(filename, content, mode=None):
    tmp = tmp_filename(filename)
    fp = open(tmp, 'x')
    fp.write(content)
    fp.flush()
    os.fsync(fp.fileno())
    if mode is not None:
        os.chmod(fp.fileno(), mode)
    os.rename(tmp, filename)
    return tmp


def backup_filename(filename, date=None):
    if date is None:
        date = datetime.date.today()
    return '.'.join([filename, 'system76-{}'.format(date)])


def update_grub():
    log.info('Calling `update-grub`...')
    SubProcess.check_call(['update-grub'])


def update_kernelstub():
    log.info('Calling `kernelstub`...')
    SubProcess.check_call(['kernelstub'])


def parse_lspci(text):
    """
    Parse output of `lspci -vmnn`.
    """
    pci = {}
    bdf =  None  # BDF: bus/device/function
    for line in text.splitlines():
        if line == '':
            bdf = None
        else:
            (name, value) = line.split(':\t')
            if name == 'Device' and bdf is None:
                bdf = value
                assert bdf not in pci
                pci[bdf] = {}
            elif name in ('Class', 'Vendor', 'Device', 'SVendor', 'SDevice', 'Rev'):
                assert bdf is not None
                key = name.lower()
                assert key not in pci[bdf]
                if name == 'Rev':
                    pci[bdf][key] = value
                else:
                    key_id = key + '_id'
                    assert key_id not in pci[bdf]
                    match = LSPCI_RE.match(value)
                    pci[bdf][key] = match.group(1)
                    pci[bdf][key_id] = match.group(2)
    return pci


CLASS_VGA = '0300'
VENDOR_NVIDIA = '10de'


def get_has_nvidia(pci):
    for (bdf, info) in pci.items():
        if info['class_id'] == CLASS_VGA and info['vendor_id'] == VENDOR_NVIDIA:
            return True
    return False


def has_nvidia():
    try:
        text = SubProcess.check_output(['lspci', '-vmnn']).decode()
        pci = parse_lspci(text)
        return get_has_nvidia(pci)
    except:
        return False


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
                log.info('Skipping %r as it was already applied', name)

        if any(action.update_grub for action in self.needed):
            if path.isfile(path.join('/', 'usr', 'bin', 'kernelstub')):
                yield _('Running `kernelstub`')
                update_kernelstub()
            else:
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
    Base class for actions that modify GRUB_CMDLINE_LINUX_DEFAULT.

    GrubAction subclasses can add and/or remove kernel boot parameters (args)
    from the GRUB_CMDLINE_LINUX_DEFAULT in /etc/default/grub.

    This works in a way that preserves customer customizations.  For example,
    an subclass that adds the "foo" and "bar" boot params:

    >>> class add_foo_bar(GrubAction):
    ...     add = ('foo', 'bar')
    ...
    ...     def describe(self):
    ...         return _('I add foo and bar')
    ...
    >>> action = add_foo_bar()
    >>> action.build_new_cmdline('quiet splash acpi_enforce_resources=lax')
    'acpi_enforce_resources=lax bar foo quiet splash'

    You can also use GrubAction to remove parameters that we previously used on
    an earlier version of the driver (and likely an earlier version of Ubuntu),
    but now are no longer needed, or in particular, now causes problems when
    present:

    >>> class remove_baz(GrubAction):
    ...     remove = ('baz',)
    ...
    ...     def describe(self):
    ...         return _('I remove baz')
    ...
    >>> action = remove_baz()
    >>> action.build_new_cmdline('quiet baz acpi_enforce_resources=lax splash')
    'acpi_enforce_resources=lax quiet splash'

    Note that to graciously accommodate customer changes, we should *only*
    remove parameters that we previously used on the exact product and are now
    problematic.
    """

    update_grub = True
    add = tuple()
    remove = tuple()
    insert_default = False

    def __init__(self, etcdir='/etc'):
        if path.isfile(path.join('/', 'usr', 'bin', 'kernelstub')):
            self.mode = 'kernelstub'
            self.filename = path.join(etcdir, 'kernelstub', 'configuration')
        else:
            self.mode = 'grub'
            self.filename = path.join(etcdir, 'default', 'grub')

    def read(self):
        return open(self.filename, 'r').read()

    def has_cmdline_default(self):
        for line in self.read().splitlines():
            match = CMDLINE_CHECK_DEFAULT_RE.match(line)
            if match:
                return True
        return False
        
    def add_cmdline_default(self, content):
        print(content)
        for line in content.splitlines():
            match = CMDLINE_ADD_DEFAULT_RE.match(line)
            if match:
                yield CMDLINE_TEMPLATE.format("")
                yield match.group(0)
            else:
                yield line
          
    def get_current_kernel_options(self):
        content = self.read()
        c = json.loads(content)
        if 'user' in c:
            if 'kernel_options' in c['default']:
                return c['user']['kernel_options']
        raise Exception('Could not parse GRUB_CMDLINE_LINUX_DEFAULT')
    
    def get_current_cmdline(self):
        for line in self.read().splitlines():
            match = CMDLINE_RE.match(line)
            if match:
                return match.group(1)
        raise Exception('Could not parse GRUB_CMDLINE_LINUX_DEFAULT')

    def build_new_cmdline(self, current):
        params = set(current.split()) - set(self.remove)
        params.update(self.add)
        return ' '.join(sorted(params))

    def iter_lines(self, content):
        for line in content.splitlines():
            match = CMDLINE_RE.match(line)
            if match:
                yield CMDLINE_TEMPLATE.format(
                    self.build_new_cmdline(match.group(1))
                )
            else:
                yield line

    def iter_lines_kernelstub(self, content):
        c = json.loads(content)
        if 'user' in c:
            if 'kernel_options' in c['default']:
                cmdline = self.build_new_cmdline(c['user']['kernel_options'])
                c['user']['kernel_options'] = cmdline
        return c

    def get_isneeded_by_set(self, params):
        assert isinstance(params, set)
        if params.intersection(self.remove):
            return True
        return not params.issuperset(self.add)

    def get_isneeded(self):
        if self.mode == 'kernelstub':
            current = self.get_current_kernel_options()
            params = set(current.split())
        elif self.has_cmdline_default():
            current = self.get_current_cmdline()
            params = set(current.split())
        else:
            self.insert_default = True
            return True
        return self.get_isneeded_by_set(params)

    def perform(self):
        content = self.read_and_backup()
        if self.mode == 'kernelstub':
            content = self.iter_lines_kernelstub(content)
            self.atomic_write(json.dumps(content, indent=2, separators=(',', ': ')))
        else:
            if self.insert_default:
                content = '\n'.join(self.add_cmdline_default(content))
            content = '\n'.join(self.iter_lines(content))
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


class disable_pm_async(FileAction):
    relpath = ('etc', 'tmpfiles.d', 'system76-disable-pm_async.conf')
    content = DISABLE_PM_ASYNC

    def describe(self):
        return _('Fix suspend issues with pm_async')


class lemu1(GrubAction):
    add = ('acpi_os_name=Linux', 'acpi_osi=')

    def describe(self):
        return _('Enable brightness hot keys')


class backlight_vendor(GrubAction):
    """
    Add acpi_backlight=vendor to GRUB_CMDLINE_LINUX_DEFAULT (for gazp9).
    """

    add = ('acpi_backlight=vendor',)

    def describe(self):
        return _('Enable brightness hot keys')


class remove_backlight_vendor(GrubAction):
    """
    Remove acpi_backlight=vendor to GRUB_CMDLINE_LINUX_DEFAULT (for gazp9).
    """

    remove = ('acpi_backlight=vendor',)

    def describe(self):
        return _('Remove brightness hot-key fix')


class nvreg_enablebacklighthandler(GrubAction):
    """
    Add NVreg_EnableBacklightHandler=1 to GRUB_CMDLINE_LINUX_DEFAULT (for serw11).
    """

    add = ('nvidia.NVreg_EnableBacklightHandler=1',)

    def describe(self):
        return _('Enable brightness hot keys')


class radeon_dpm(GrubAction):
    """
    Add radeon.dpm=1 to GRUB_CMDLINE_LINUX_DEFAULT (for panp7).
    """

    add = ('radeon.dpm=1',)

    def describe(self):
        return _('Enable Radeon GPU power management')


class disable_power_well(GrubAction):
    """
    Add i915.disable_power_well=0 to GRUB_CMDLINE_LINUX_DEFAULT.

    This fixes the HDMI playback speed issue on Intel Haswell GPUs (playback
    speed is faster than it should be, aka the "chipmunk problem").
    """

    add = ('i915.disable_power_well=0',)

    def describe(self):
        return _('Fix HDMI audio playback speed')


class i915_alpha_support(GrubAction):
    """
    Add `i915.alpha_support=1` to GRUB_CMDLINE_LINUX_DEFAULT.
    """

    add = ('i915.alpha_support=1',)

    def describe(self):
        return _('Enable Intel i915 Alpha Driver Support')

    def get_isneeded(self):
        if has_nvidia():
            return False
        return super().get_isneeded()


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


class i8042_reset_nomux(GrubAction):
    """
    Add i8042.reset and i8042.nomux to GRUB_CMDLINE_LINUX_DEFAULT

    This fixes the touchpad on the oryp2 and oryp2-ess.
    """

    add = ('i8042.reset', 'i8042.nomux',)

    def describe(self):
        return _('Enable Touchpad')


class gfxpayload_text(Action):
    update_grub = True
    comment = '# Added by system76-driver:'
    prefix = 'GRUB_GFXPAYLOAD_LINUX='
    value = prefix + 'text'

    def __init__(self, etcdir='/etc'):
        self.filename = path.join(etcdir, 'default', 'grub')

    def read(self):
        return open(self.filename, 'r').read()

    def describe(self):
        return _('Improve graphics UX for UEFI resume')

    def get_isneeded(self):
        return self.value not in self.read().splitlines()

    def get_output_lines(self):
        output_lines = []
        for rawline in self.read_and_backup().splitlines():
            line = rawline.strip()
            if line != self.comment and not line.startswith(self.prefix):
                output_lines.append(rawline)
        while output_lines and output_lines[-1].strip() == '':
            output_lines.pop()
        output_lines.extend(['', self.comment, self.value, ''])
        return output_lines

    def perform(self):
        content = '\n'.join(self.get_output_lines())
        self.atomic_write(content)


class remove_gfxpayload_text(gfxpayload_text):
    def describe(self):
        return _('Remove GRUB_GFXPAYLOAD_LINUX=text line')

    def get_isneeded(self):
        lines = self.read().splitlines()
        return self.value in lines or self.comment in lines

    def get_output_lines(self):
        output_lines = []
        for rawline in self.read_and_backup().splitlines():
            line = rawline.strip()
            if line not in (self.value, self.comment):
                output_lines.append(rawline)
        while output_lines and output_lines[-1].strip() == '':
            output_lines.pop()
        output_lines.extend([''])
        return output_lines


class uvcquirks(FileAction):
    relpath = ('etc', 'modprobe.d', 'uvc.conf')
    content = 'options uvcvideo quirks=2'

    def describe(self):
        return _('Webcam quirk fixes')


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


class pulseaudio_hp_spdif_desc(FileAction):
    relpath = ('usr', 'share', 'pulseaudio', 'alsa-mixer', 'paths',
                    'iec958-stereo-output.conf')

    _content = None

    @property
    def content(self):
        if self._content is None:
            fp = open(get_datafile('iec958-stereo-output.conf'), 'r')
            self._content = fp.read()
        return self._content

    def describe(self):
        return _('Fix Headphone/SPDIF description in Pulseaudio')


DAC_PATCH = """[codec]
0x{vendor_id:08x} 0x{subsystem_id:08x} 0

[pincfg]
0x1b 0x01111060

[verb]
0x1b 0x707 0x0004
"""

DAC_MODPROBE = 'options snd-hda-intel patch=system76-audio-patch\n'


def read_hda_id(name, device='hwC0D0', rootdir='/'):
    if name not in ('vendor_id', 'subsystem_id'):
        raise ValueError('bad name: {!r}'.format(name))
    filename = path.join(rootdir, 'sys', 'class', 'sound', device, name)
    try:
        with open(filename, 'r') as fp:
            return int(fp.read(), 16)
    except FileNotFoundError:
        return 0


class dac_fixup(Action):
    relpath1 = ('lib', 'firmware', 'system76-audio-patch')
    relpath2 = ('etc', 'modprobe.d', 'system76-alsa-base.conf')

    def __init__(self, rootdir='/'):
        self.filename1 = path.join(rootdir, *self.relpath1)
        self.filename2 = path.join(rootdir, *self.relpath2)
        self.vendor_id = read_hda_id('vendor_id', rootdir=rootdir)
        self.subsystem_id = read_hda_id('subsystem_id', rootdir=rootdir)
        self.content1 = DAC_PATCH.format(
            vendor_id=self.vendor_id,
            subsystem_id=self.subsystem_id,
        )
        self.content2 = DAC_MODPROBE

    def read1(self):
        try:
            return open(self.filename1, 'r').read()
        except FileNotFoundError:
            return None

    def read2(self):
        try:
            return open(self.filename2, 'r').read()
        except FileNotFoundError:
            return None

    def get_isneeded(self):
        return self.read1() != self.content1 or self.read2() != self.content2

    def perform(self):
        atomic_write(self.filename1, self.content1)
        atomic_write(self.filename2, self.content2)

    def describe(self):
        return _('Enable high-quality audio DAC')


HEADSET_PATCH = """[codec]
0x{vendor_id:08x} 0x{subsystem_id:08x} 0

[pincfg]
0x19 0x23A11040
"""

HEADSET_MODPROBE = 'options snd-hda-intel patch=system76-audio-patch\n'


class headset_fixup(Action):
    relpath1 = ('lib', 'firmware', 'system76-audio-patch')
    relpath2 = ('etc', 'modprobe.d', 'system76-alsa-base.conf')

    def __init__(self, rootdir='/'):
        self.filename1 = path.join(rootdir, *self.relpath1)
        self.filename2 = path.join(rootdir, *self.relpath2)
        self.vendor_id = read_hda_id('vendor_id', rootdir=rootdir)
        self.subsystem_id = read_hda_id('subsystem_id', rootdir=rootdir)
        self.content1 = HEADSET_PATCH.format(
            vendor_id=self.vendor_id,
            subsystem_id=self.subsystem_id,
        )
        self.content2 = HEADSET_MODPROBE

    def read1(self):
        try:
            return open(self.filename1, 'r').read()
        except FileNotFoundError:
            return None

    def read2(self):
        try:
            return open(self.filename2, 'r').read()
        except FileNotFoundError:
            return None

    def get_isneeded(self):
        return self.read1() != self.content1 or self.read2() != self.content2

    def perform(self):
        atomic_write(self.filename1, self.content1)
        atomic_write(self.filename2, self.content2)

    def describe(self):
        return _('Enable headset microphone')


def get_distribution():
    try:
        #path = path.join('/', 'etc', 'lsb-release')
        #with open(path, 'r') as fp:
        cmd = ['lsb_release', '-a']
        content = subprocess.check_output(cmd).decode('utf-8')
        for line in content.splitlines():
            pair = line.strip('\n').split(':', 1)
            if len(pair) != 2:
                continue
            key = pair[0]
            value = pair[1].lstrip()
            if key == 'Description':
                print(value)
                if value.startswith('Ubuntu'):
                    return 'Ubuntu'
                elif value.startswith('Pop!_OS'):
                    return 'Pop'
                else:
                    return 'Unknown'
    except:
        pass
    return ''


ENERGYSTAR_GSETTINGS_OVERRIDE = """[org.gnome.settings-daemon.plugins.power]
sleep-inactive-ac-type='suspend'
sleep-inactive-ac-timeout=1800
"""

class energystar_gsettings_override(FileAction):
    relpath = ('usr', 'share', 'glib-2.0', 'schemas',
        '50_system76-driver-energystar.gschema.override')

    _content = ENERGYSTAR_GSETTINGS_OVERRIDE

    @property
    def content(self):
        return self._content

    def perform(self):
        self.atomic_write(self.content, self.mode)
        gsettings_dir = path.join('/', 'usr', 'share', 'glib-2.0', 'schemas')
        cmd_compile_schemas = ['glib-compile-schemas', gsettings_dir + '/']
        SubProcess.check_call(cmd_compile_schemas)

    def get_isneeded(self):
        if get_distribution != 'Ubuntu':
            return False
        if self.read() != self.content:
            return True
        st = os.stat(self.filename)
        if stat.S_IMODE(st.st_mode) != self.mode:
            return True
        return False

    def describe(self):
        return _('Apply ENERGY STAR default gsettings overrides')


ENERGYSTAR_WAKEONLAN_SCRIPT = """#!/usr/bin/env bash

set -e

for d in /sys/class/net/*/ ; do
    if [[ $(basename $d) == en* ]]; then
        ethtool -s $(basename $d) wol $1
    fi
done
"""

ENERGYSTAR_WAKEONLAN_RULE = """# AC PLUGGED-IN
SUBSYSTEM=="power_supply", ATTR{online}=="1", RUN+="/usr/lib/system76-driver/system76-wakeonlan g"

# ON BATTERY
SUBSYSTEM=="power_supply", ATTR{online}=="0", RUN+="/usr/lib/system76-driver/system76-wakeonlan d"
"""

class energystar_wakeonlan(FileAction):
    relpath1 = ('usr', 'lib', 'system76-driver',
        'system76-wakeonlan')
    relpath2 = ('etc', 'udev', 'rules.d',
        '10-system76-driver-energystar-wakeonlan.rules')

    content1 = ENERGYSTAR_WAKEONLAN_SCRIPT
    content2 = ENERGYSTAR_WAKEONLAN_RULE
    
    mode1 = 0o755

    def __init__(self, rootdir='/'):
        self.filename1 = path.join(rootdir, *self.relpath1)
        self.filename2 = path.join(rootdir, *self.relpath2)

    def read1(self):
        try:
            return open(self.filename1, 'r').read()
        except FileNotFoundError:
            return None

    def read2(self):
        try:
            return open(self.filename2, 'r').read()
        except FileNotFoundError:
            return None

    def get_isneeded(self):
        if get_distribution != 'Ubuntu':
            return False
        return self.read1() != self.content1 or self.read2() != self.content2

    def perform(self):
        atomic_write(self.filename1, self.content1, mode=self.mode1)
        atomic_write(self.filename2, self.content2)

    def describe(self):
        return _('Disable Wake-On-LAN on battery power for ENERGY STAR')


DPI_DEFAULT = 96

DPI_LIMIT = 170

HIDPI_GSETTINGS_OVERRIDE = ["""[com.ubuntu.user-interface]
scale-factor={'""", """': 16}
"""]

CONSOLE_SETUP_CONTENT = """# CONFIGURATION FILE FOR SETUPCON

# Consult the console-setup(5) manual page.

ACTIVE_CONSOLES="/dev/tty[1-6]"

CHARMAP="UTF-8"

CODESET="guess"
FONTFACE="Terminus"
FONTSIZE="16x32"

VIDEOMODE=

# The following is an example how to use a braille font
# FONT='lat9w-08.psf.gz brl-8x8.psf'"""

class hidpi_scaling(FileAction):
    relpath = ('usr', 'share', 'glib-2.0', 'schemas',
        '90_system76-driver-hidpi.gschema.override')
    content = HIDPI_GSETTINGS_OVERRIDE[0] + "DP-0" + HIDPI_GSETTINGS_OVERRIDE[1]

    console_setup_content = CONSOLE_SETUP_CONTENT
    console_setup_mode = 0o644

    def __init__(self, rootdir='/'):
        self.filename = path.join(rootdir, *self.relpath)

    def needs_hidpi_scaling(self):
        cmd = ['xrandr']

        try:
            xrandr_output = SubProcess.check_output(cmd)
            xrandr_string = xrandr_output.decode("utf-8")
        except:
            log.info('failed to call xrandr: Please run system76-driver-cli while X is running')
            return False

        try:
            # Check if DP-0 exists
            reg = re.compile(r'^(DP-0|eDP-1)\b', re.MULTILINE)
            if not reg.findall(str(xrandr_string)):
                log.info('Could not find internal display in xrandr.')
                return False

            # Retrieve physical display dimensions and screen resolution
            # Picks first resolution entry, may not be the native or current one
            reg = re.compile(r'''^(DP-0|eDP-1)\b            # Find the entry for DP-0
                            .*?
                            (\d+)mm\ x\ (\d+)mm # Get the physical dimensions
                            \s*\n\s*
                            (\d+)x(\d+)         # Get screen resolution
                            ''',
                            flags=re.VERBOSE | re.MULTILINE)
            xrandr_tokens = reg.findall(xrandr_string)
            display_name, width_mm, height_mm, width_pix, height_pix = xrandr_tokens[0]
        except:
            log.info('Failed to retrieve display size and resolution.')
            return False

        dpi_x = 0.0
        dpi_y = 0.0
        if (width_mm == 0 or height_mm == 0):
            dpi_x = DPI_DEFAULT
            dpi_y = DPI_DEFAULT
        else:
            dpi_x = 25.4 * int(width_pix) / int(width_mm)
            dpi_y = 25.4 * int(height_pix) / int(height_mm)

        if (dpi_x > DPI_LIMIT or dpi_y > DPI_LIMIT):
            self.content = HIDPI_GSETTINGS_OVERRIDE[0] + display_name + HIDPI_GSETTINGS_OVERRIDE[1]
            return True
        return False

    def get_isneeded(self):
        needed = False
        if self.read() != self.content:
            needed = True
        else:
            st = os.stat(self.filename)
            if stat.S_IMODE(st.st_mode) != self.mode:
                needed = True
        if needed:
            return self.needs_hidpi_scaling()
        return False

    def perform(self):
        self.atomic_write(self.content, self.mode)
        gsettings_dir = path.join('/', 'usr', 'share', 'glib-2.0', 'schemas')
        cmd_compile_schemas = ['glib-compile-schemas', gsettings_dir + '/']
        SubProcess.check_call(cmd_compile_schemas)

        # Configure default console font
        # (only if we know we haven't set it before)
        self.console_setup_filename = path.join('/',
            'etc', 'default', 'console-setup')
        atomic_write(self.console_setup_filename,
            self.console_setup_content,
            self.console_setup_mode
        )


    def describe(self):
        return _('Set default HiDPI scaling factor.')

