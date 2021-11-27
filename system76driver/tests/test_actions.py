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
Unit tests for `system76driver.actions` module.
"""

from unittest import TestCase
import os
from os import path
import stat
from base64 import b32decode, b32encode
from random import SystemRandom

from .helpers import TempDir
from system76driver.mockable import SubProcess
from system76driver import actions


random = SystemRandom()


GRUB = """
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.
# For full documentation of the options in this file, see:
#   info -f grub -n 'Simple configuration'

GRUB_DEFAULT=0
GRUB_HIDDEN_TIMEOUT=0
GRUB_HIDDEN_TIMEOUT_QUIET=true
GRUB_TIMEOUT=10
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="{}"
GRUB_CMDLINE_LINUX=""

# Uncomment to enable BadRAM filtering, modify to suit your needs
# This works with Linux (no patch required) and with any kernel that obtains
# the memory map information from GRUB (GNU Mach, kernel of FreeBSD ...)
#GRUB_BADRAM="0x01234567,0xfefefefe,0x89abcdef,0xefefefef"

# Uncomment to disable graphical terminal (grub-pc only)
#GRUB_TERMINAL=console

# The resolution used on graphical terminal
# note that you can use only modes which your graphic card supports via VBE
# you can see them in real GRUB with the command `vbeinfo'
#GRUB_GFXMODE=640x480

# Uncomment if you don't want GRUB to pass "root=UUID=xxx" parameter to Linux
#GRUB_DISABLE_LINUX_UUID=true

# Uncomment to disable generation of recovery mode menu entries
#GRUB_DISABLE_RECOVERY="true"

# Uncomment to get a beep at grub start
#GRUB_INIT_TUNE="480 440 1"
""".strip()

GRUB_ORIG = GRUB.format('quiet splash')


class TestFunctions(TestCase):
    def test_random_id(self):
        _id = actions.random_id()
        self.assertIsInstance(_id, str)
        self.assertEqual(len(_id), 24)
        self.assertEqual(b32encode(b32decode(_id)).decode('utf-8'), _id)
        _id = actions.random_id(numbytes=10)
        self.assertIsInstance(_id, str)
        self.assertEqual(len(_id), 16)
        self.assertEqual(b32encode(b32decode(_id)).decode('utf-8'), _id)
        accum = set(actions.random_id() for i in range(100))
        self.assertEqual(len(accum), 100)

    def test_tmp_filename(self):
        tmp = actions.tmp_filename('/foo/bar')
        (base, random) = tmp.split('.')
        self.assertEqual(base, '/foo/bar')
        self.assertEqual(len(random), 24)
        self.assertEqual(b32encode(b32decode(random)).decode('utf-8'), random)

    def test_update_grub(self):
        SubProcess.reset(mocking=True)
        self.assertIsNone(actions.update_grub())
        self.assertEqual(SubProcess.calls, [
            ('check_call', ['update-grub'], {}),
        ])

    def test_read_hda_id(self):
        NAMES = ('vendor_id', 'subsystem_id')
        VALUES = (
            random.randint(1, 0xffffffff),
            random.randint(1, 0xffffffff),
        )
        PAIRS = tuple(zip(NAMES, VALUES))
        tmp = TempDir()

        # Directories and files missing:
        for name in NAMES:
            self.assertEqual(actions.read_hda_id(name, rootdir=tmp.dir), 0)

        # Files missing:
        tmp.makedirs('sys', 'class', 'sound', 'hwC0D0')
        for name in NAMES:
            self.assertEqual(actions.read_hda_id(name, rootdir=tmp.dir), 0)

        # Files are present:
        for (name, value) in PAIRS:
            self.assertNotEqual(value, 0)
            content = '0x{:08x}\n'.format(value).encode()
            self.assertEqual(len(content), 11)
            tmp.write(content, 'sys', 'class', 'sound', 'hwC0D0', name)
            self.assertEqual(actions.read_hda_id(name, rootdir=tmp.dir), value)

        # Bad name:
        with self.assertRaises(ValueError) as cm:
            actions.read_hda_id('foo_id', rootdir=tmp.dir)
        self.assertEqual(str(cm.exception),
            "bad name: 'foo_id'"
        )


class TestAction(TestCase):
    def test_isneeded(self):
        a = actions.Action()
        a._isneeded = True
        self.assertIs(a.isneeded, True)
        a._isneeded = False
        self.assertIs(a.isneeded, False)
        a._isneeded = None
        with self.assertRaises(NotImplementedError) as cm:
            a.isneeded
        self.assertEqual(str(cm.exception), 'Action.get_isneeded()')

    def test_description(self):
        a = actions.Action()
        a._description = 'Driver for stuff'
        self.assertEqual(a.description, 'Driver for stuff')
        desc = actions.random_id()
        a._description = desc
        self.assertIs(a.description, desc)
        a._description = None
        with self.assertRaises(NotImplementedError) as cm:
            a.description
        self.assertEqual(str(cm.exception), 'Action.describe()')

    def test_describe(self):
        a = actions.Action()
        with self.assertRaises(NotImplementedError) as cm:
            a.describe()
        self.assertEqual(str(cm.exception), 'Action.describe()')

        class Example(actions.Action):
            pass

        a = Example()
        with self.assertRaises(NotImplementedError) as cm:
            a.describe()
        self.assertEqual(str(cm.exception), 'Example.describe()')

    def test_get_isneeded(self):
        a = actions.Action()
        with self.assertRaises(NotImplementedError) as cm:
            a.get_isneeded()
        self.assertEqual(str(cm.exception), 'Action.get_isneeded()')

        class Example(actions.Action):
            pass

        a = Example()
        with self.assertRaises(NotImplementedError) as cm:
            a.get_isneeded()
        self.assertEqual(str(cm.exception), 'Example.get_isneeded()')

    def test_perform(self):
        a = actions.Action()
        with self.assertRaises(NotImplementedError) as cm:
            a.perform()
        self.assertEqual(str(cm.exception), 'Action.perform()')

        class Example(actions.Action):
            pass

        a = Example()
        with self.assertRaises(NotImplementedError) as cm:
            a.perform()
        self.assertEqual(str(cm.exception), 'Example.perform()')


class NeededAction(actions.Action):
    def get_isneeded(self):
        return True


class UnneededAction(actions.Action):
    def get_isneeded(self):
        return False


class TestActionRunner(TestCase):
    def test_init(self):
        klasses = [UnneededAction, NeededAction]
        inst = actions.ActionRunner(klasses)
        self.assertIs(inst.klasses, klasses)
        self.assertEqual(inst.klasses, [UnneededAction, NeededAction])
        self.assertIsInstance(inst.actions, list)
        self.assertEqual(len(inst.actions), 2)
        self.assertIsInstance(inst.actions[0], UnneededAction)
        self.assertIsInstance(inst.actions[1], NeededAction)
        self.assertIsInstance(inst.needed, list)
        self.assertEqual(len(inst.needed), 1)
        self.assertIsInstance(inst.needed[0], NeededAction)


class TestFileAction(TestCase):
    def test_init(self):
        class Example(actions.FileAction):
            relpath = ('foo', 'bar', 'baz')

        tmp = TempDir()
        inst = actions.FileAction()
        self.assertEqual(inst.filename, '/')
        inst = actions.FileAction(rootdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.dir)
        inst = Example()
        self.assertEqual(inst.filename, '/foo/bar/baz')
        inst = Example(rootdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.join('foo', 'bar', 'baz'))

    def test_read(self):
        tmp = TempDir()
        name = tmp.join('some', 'file')
        inst = actions.FileAction()
        inst.filename = name
        self.assertIsNone(inst.read())
        tmp.mkdir('some')
        self.assertIsNone(inst.read())
        open(name, 'x').write('foo\nbar\n')
        self.assertEqual(inst.read(), 'foo\nbar\n')

    def test_get_isneeded(self):
        class Example(actions.FileAction):
            relpath = ('some', 'file')
            content = 'foo'

        tmp = TempDir()
        inst = Example(rootdir=tmp.dir)

        # Missing parentdir:
        self.assertIs(inst.get_isneeded(), True)

        # Missing file:
        tmp.mkdir('some')
        self.assertIs(inst.get_isneeded(), True)

        # Wrong content:
        open(inst.filename, 'x').write('bar')
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), True)

        # Wrong permissions:
        open(inst.filename, 'w').write('foo')
        os.chmod(inst.filename, 0o600)
        self.assertIs(inst.get_isneeded(), True)
        os.chmod(inst.filename, 0o666)
        self.assertIs(inst.get_isneeded(), True)

        # Not needed:
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), False)

    def _check_file(self, inst):
        self.assertEqual(open(inst.filename, 'r').read(), 'foo')
        st = os.stat(inst.filename)
        self.assertEqual(stat.S_IMODE(st.st_mode), 0o600)

    def test_perform(self):
        class Example(actions.FileAction):
            relpath = ('some', 'file')
            content = 'foo'
            mode = 0o600

        tmp = TempDir()
        inst = Example(rootdir=tmp.dir)

        # Missing parentdir:
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Missing file:
        tmp.remove(inst.filename)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Wrong content:
        open(inst.filename, 'w').write('bar')
        os.chmod(inst.filename, 0o600)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Wrong permissions:
        open(inst.filename, 'w').write('foo')
        os.chmod(inst.filename, 0o444)
        self.assertIsNone(inst.perform())
        self._check_file(inst)
        os.chmod(inst.filename, 0o666)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Not needed:
        os.chmod(inst.filename, 0o644)
        self.assertIsNone(inst.perform())
        self._check_file(inst)


class TestGrubAction(TestCase):
    def test_init(self):
        inst = actions.GrubAction()
        self.assertIs(inst.update_grub, True)
        self.assertIn(inst.mode, ['kernelstub', 'grub'])
        if inst.mode == 'kernelstub':
            self.assertEqual(inst.filename, '/etc/kernelstub/configuration')
        elif inst.mode == 'grub':
            self.assertEqual(inst.filename, '/etc/default/grub')
        self.assertEqual(inst.add, tuple())
        self.assertEqual(inst.remove, tuple())

        tmp = TempDir()
        inst = actions.GrubAction(etcdir=tmp.dir)
        self.assertIs(inst.update_grub, True)
        self.assertIn(inst.mode, ['kernelstub', 'grub'])
        if inst.mode == 'kernelstub':
            self.assertEqual(inst.filename, tmp.join('kernelstub', 'configuration'))
        elif inst.mode == 'grub':
            self.assertEqual(inst.filename, tmp.join('default', 'grub'))
        self.assertEqual(inst.add, tuple())
        self.assertEqual(inst.remove, tuple())

    def test_read(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.read()
        self.assertEqual(cm.exception.filename, inst.filename)
        if inst.mode == 'grub':
            tmp.write(b'foobar\n', 'default', 'grub')
            self.assertEqual(inst.read(), 'foobar\n')

    def test_get_current_cmdline(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)

        # Missing file:
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_current_cmdline()
        self.assertEqual(cm.exception.filename, inst.filename)

        if inst.mode == 'grub':
            # Bad content:
            open(inst.filename, 'x').write('wont work\n')
            with self.assertRaises(Exception) as cm:
                inst.get_current_cmdline()
            self.assertEqual(str(cm.exception),
                'Could not parse GRUB_CMDLINE_LINUX_DEFAULT'
            )

            # Good content:
            open(inst.filename, 'w').write(GRUB_ORIG)
            self.assertEqual(inst.get_current_cmdline(), 'quiet splash')
            open(inst.filename, 'w').write(
                GRUB.format('acpi_os_name=Linux acpi_osi=')
            )
            self.assertEqual(inst.get_current_cmdline(),
                'acpi_os_name=Linux acpi_osi='
            )

    def test_build_new_cmdline(self):
        inst = actions.GrubAction()
        self.assertEqual(
            inst.build_new_cmdline('world hello'),
            'world hello'
        )

        class Subclass(actions.GrubAction):
            add = ('nurse', 'naughty', 'hello')
            remove = ('other', 'world')

        inst = Subclass()
        self.assertEqual(
            inst.build_new_cmdline('world hello'),
            'hello nurse naughty'
        )
        self.assertEqual(
            inst.build_new_cmdline('naughty nurse hello'),
            'naughty nurse hello'
        )

    def test_iter_lines(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            content = inst.read_and_backup()
            list(inst.iter_lines(content))
        self.assertEqual(cm.exception.filename, inst.filename)

        if inst.mode == 'grub':
            open(inst.filename, 'x').write(GRUB_ORIG)
            content = inst.read_and_backup()
            self.assertEqual('\n'.join(inst.iter_lines(content)), GRUB_ORIG)
            self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)
            self.assertEqual(inst.bak, actions.backup_filename(inst.filename))

            open(inst.filename, 'w').write(
                GRUB.format('foo bar aye')
            )
            content = inst.read_and_backup()
            self.assertEqual(
                '\n'.join(inst.iter_lines(content)),
                GRUB.format('foo bar aye')
            )
            self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)

        # Test subclass with different GrubAction.cmdline:
        class Example(actions.GrubAction):
            add = ('acpi_os_name=Linux', 'acpi_osi=')

        tmp = TempDir()
        tmp.mkdir('default')
        inst = Example(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            content = inst.read_and_backup()
            list(inst.iter_lines(content))
        self.assertEqual(cm.exception.filename, inst.filename)

        if inst.mode == 'grub':
            open(inst.filename, 'x').write(GRUB_ORIG)
            content = inst.read_and_backup()
            self.assertEqual(
                '\n'.join(inst.iter_lines(content)),
                GRUB.format('quiet splash acpi_os_name=Linux acpi_osi=')
            )
            self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)
            self.assertEqual(inst.bak, actions.backup_filename(inst.filename))

            content = inst.read_and_backup()
            self.assertEqual(
                '\n'.join(inst.iter_lines(content)),
                GRUB.format('quiet splash acpi_os_name=Linux acpi_osi=')
            )
            self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)

    def test_get_isneeded_by_set(self):
        inst = actions.GrubAction()
        self.assertIs(inst.get_isneeded_by_set(set()), False)
        self.assertIs(inst.get_isneeded_by_set({'foo'}), False)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar'}), False)

        # Test when subclass has add:
        class Subclass(actions.GrubAction):
            add = ('foo', 'bar')

        inst = Subclass()
        self.assertIs(inst.get_isneeded_by_set(set()), True)
        self.assertIs(inst.get_isneeded_by_set({'foo'}), True)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar'}), False)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar', 'baz'}), False)
        self.assertIs(inst.get_isneeded_by_set({'baz'}), True)

        # Test when subclass has remove:
        class Subclass(actions.GrubAction):
            remove = ('foo', 'bar')

        inst = Subclass()
        self.assertIs(inst.get_isneeded_by_set(set()), False)
        self.assertIs(inst.get_isneeded_by_set({'foo'}), True)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar'}), True)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar', 'baz'}), True)
        self.assertIs(inst.get_isneeded_by_set({'baz'}), False)

        # Test when subclass has add *and* remove:
        class Subclass(actions.GrubAction):
            add = ('foo', 'bar')
            remove = ('haz', 'fez')

        inst = Subclass()
        self.assertIs(inst.get_isneeded_by_set(set()), True)
        self.assertIs(inst.get_isneeded_by_set({'moo'}), True)
        self.assertIs(inst.get_isneeded_by_set({'foo'}), True)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar'}), False)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar', 'moo'}), False)

        self.assertIs(inst.get_isneeded_by_set({'haz'}), True)
        self.assertIs(inst.get_isneeded_by_set({'haz', 'fez'}), True)
        self.assertIs(inst.get_isneeded_by_set({'haz', 'fez', 'moo'}), True)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar', 'haz'}), True)
        self.assertIs(inst.get_isneeded_by_set({'foo', 'bar', 'haz', 'fez'}), True)

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        if inst.mode == 'grub':
            open(inst.filename, 'x').write(GRUB_ORIG)
            self.assertIs(inst.get_isneeded(), False)
            open(inst.filename, 'w').write(
                GRUB.format('acpi_os_name=Linux acpi_osi=')
            )
            self.assertIs(inst.get_isneeded(), False)

        # Test subclass with different GrubAction.cmdline:
        class Example(actions.GrubAction):
            add = ('acpi_os_name=Linux', 'acpi_osi=')

        tmp = TempDir()
        tmp.mkdir('default')
        inst = Example(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        if inst.mode == 'grub':
            open(inst.filename, 'x').write(GRUB_ORIG)
            self.assertIs(inst.get_isneeded(), True)
            open(inst.filename, 'w').write(
                GRUB.format('acpi_os_name=Linux acpi_osi=')
            )
            self.assertIs(inst.get_isneeded(), False)

    def test_perform(self):
        SubProcess.reset(mocking=True)

        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)

        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)

        if inst.mode == 'grub':
            with open(inst.filename, 'x') as fp:
                fp.write(GRUB_ORIG)
            self.assertIsNone(inst.perform())
            self.assertEqual(open(inst.filename, 'r').read(), GRUB_ORIG)

            with open(inst.filename, 'w') as fp:
                fp.write(GRUB.format('c a b'))
            self.assertIsNone(inst.perform())
            self.assertEqual(open(inst.filename, 'r').read(), GRUB.format('c a b'))

            self.assertEqual(SubProcess.calls, [])

        # Test subclass with different GrubAction.cmdline:
        class Example(actions.GrubAction):
            add = ('foo', 'bar')

        tmp = TempDir()
        tmp.mkdir('default')
        inst = Example(etcdir=tmp.dir)

        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)

        if inst.mode == 'grub':
            with open(inst.filename, 'x') as fp:
                fp.write(GRUB_ORIG)
            self.assertIsNone(inst.perform())
            self.assertEqual(
                open(inst.filename, 'r').read(),
                GRUB.format('quiet splash foo bar')
            )

            self.assertIsNone(inst.perform())
            self.assertEqual(
                open(inst.filename, 'r').read(),
                GRUB.format('quiet splash foo bar')
            )

            self.assertEqual(SubProcess.calls, [])


class Test_wifi_pm_disable(TestCase):
    def test_init(self):
        inst = actions.wifi_pm_disable()
        self.assertEqual(inst.filename, '/etc/pm/power.d/wireless')

        tmp = TempDir()
        inst = actions.wifi_pm_disable(rootdir=tmp.dir)
        self.assertEqual(inst.filename,
            tmp.join('etc', 'pm', 'power.d', 'wireless')
        )

    def test_read(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'power.d')
        inst = actions.wifi_pm_disable(rootdir=tmp.dir)
        self.assertIsNone(inst.read())
        tmp.write(b'Hello, World', 'etc', 'pm', 'power.d', 'wireless')
        self.assertEqual(inst.read(), 'Hello, World')

    def test_describe(self):
        inst = actions.wifi_pm_disable()
        self.assertEqual(inst.describe(), 'Improve WiFi performance on Battery')

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'power.d')
        inst = actions.wifi_pm_disable(rootdir=tmp.dir)

        # Missing file
        self.assertIs(inst.get_isneeded(), True)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o755)
        self.assertIs(inst.get_isneeded(), True)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(actions.WIFI_PM_DISABLE)
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), True)
        os.chmod(inst.filename, 0o777)
        self.assertIs(inst.get_isneeded(), True)

        # All good:
        os.chmod(inst.filename, 0o755)
        self.assertIs(inst.get_isneeded(), False)

    def _check_file(self, inst):
        self.assertEqual(
            open(inst.filename, 'r').read(),
            actions.WIFI_PM_DISABLE
        )
        st = os.stat(inst.filename)
        self.assertEqual(stat.S_IMODE(st.st_mode), 0o755)

    def test_perform(self):
        tmp = TempDir()
        inst = actions.wifi_pm_disable(rootdir=tmp.dir)

        # Missing directories
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Missing file
        tmp.remove(inst.filename)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o755)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(actions.WIFI_PM_DISABLE)
        os.chmod(inst.filename, 0o644)
        self.assertIsNone(inst.perform())
        self._check_file(inst)
        os.chmod(inst.filename, 0o000)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Action didn't need to be performed:
        self.assertIsNone(inst.perform())
        self._check_file(inst)


class Test_hdmi_hotplug_fix(TestCase):
    def test_init(self):
        inst = actions.hdmi_hotplug_fix()
        self.assertEqual(inst.filename, '/etc/pm/power.d/audio')

        tmp = TempDir()
        inst = actions.hdmi_hotplug_fix(rootdir=tmp.dir)
        self.assertEqual(inst.filename,
            tmp.join('etc', 'pm', 'power.d', 'audio')
        )

    def test_read(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'power.d')
        inst = actions.hdmi_hotplug_fix(rootdir=tmp.dir)
        self.assertIsNone(inst.read())
        tmp.write(b'Hello, World', 'etc', 'pm', 'power.d', 'audio')
        self.assertEqual(inst.read(), 'Hello, World')

    def test_describe(self):
        inst = actions.hdmi_hotplug_fix()
        self.assertEqual(inst.describe(), 'Fix HDMI hot-plugging when on battery')

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'power.d')
        inst = actions.hdmi_hotplug_fix(rootdir=tmp.dir)

        # Missing file
        self.assertIs(inst.get_isneeded(), True)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o755)
        self.assertIs(inst.get_isneeded(), True)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(actions.HDMI_HOTPLUG_FIX)
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), True)
        os.chmod(inst.filename, 0o777)
        self.assertIs(inst.get_isneeded(), True)

        # All good:
        os.chmod(inst.filename, 0o755)
        self.assertIs(inst.get_isneeded(), False)

    def _check_file(self, inst):
        self.assertEqual(
            open(inst.filename, 'r').read(),
            actions.HDMI_HOTPLUG_FIX
        )
        st = os.stat(inst.filename)
        self.assertEqual(stat.S_IMODE(st.st_mode), 0o755)

    def test_perform(self):
        tmp = TempDir()
        inst = actions.hdmi_hotplug_fix(rootdir=tmp.dir)

        # Missing directories
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Missing file
        tmp.remove(inst.filename)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o755)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(actions.HDMI_HOTPLUG_FIX)
        os.chmod(inst.filename, 0o644)
        self.assertIsNone(inst.perform())
        self._check_file(inst)
        os.chmod(inst.filename, 0o000)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Action didn't need to be performed:
        self.assertIsNone(inst.perform())
        self._check_file(inst)


class Test_disable_pm_async(TestCase):
    def test_init(self):
        inst = actions.disable_pm_async()
        self.assertEqual(inst.filename, '/etc/tmpfiles.d/system76-disable-pm_async.conf')

        tmp = TempDir()
        inst = actions.disable_pm_async(rootdir=tmp.dir)
        self.assertEqual(inst.filename,
            tmp.join('etc', 'tmpfiles.d', 'system76-disable-pm_async.conf')
        )

    def test_read(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'tmpfiles.d')
        inst = actions.disable_pm_async(rootdir=tmp.dir)
        self.assertIsNone(inst.read())
        tmp.write(b'Hello, World', 'etc', 'tmpfiles.d', 'system76-disable-pm_async.conf')
        self.assertEqual(inst.read(), 'Hello, World')

    def test_describe(self):
        inst = actions.disable_pm_async()
        self.assertEqual(inst.describe(), 'Fix suspend issues with pm_async')

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'tmpfiles.d')
        inst = actions.disable_pm_async(rootdir=tmp.dir)

        # Missing file
        self.assertIs(inst.get_isneeded(), True)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), True)

        # All good:
        open(inst.filename, 'w').write(actions.DISABLE_PM_ASYNC)
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), False)

    def _check_file(self, inst):
        self.assertEqual(
            open(inst.filename, 'r').read(),
            actions.DISABLE_PM_ASYNC
        )
        st = os.stat(inst.filename)
        self.assertEqual(stat.S_IMODE(st.st_mode), 0o644)

    def test_perform(self):
        tmp = TempDir()
        inst = actions.disable_pm_async(rootdir=tmp.dir)

        # Missing directories
        self.assertIsNone(inst.perform())

        # Missing file
        tmp.remove(inst.filename)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(actions.DISABLE_PM_ASYNC)
        os.chmod(inst.filename, 0o755)
        self.assertIsNone(inst.perform())
        self._check_file(inst)
        os.chmod(inst.filename, 0o000)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Action didn't need to be performed:
        self.assertIsNone(inst.perform())
        self._check_file(inst)


class Test_lemu1(TestCase):
    def test_decribe(self):
        inst = actions.lemu1()
        self.assertEqual(inst.describe(),
            'Enable brightness hot keys'
        )

    def test_build_new_cmdline(self):
        inst = actions.lemu1()
        self.assertEqual(inst.add,
            ('acpi_os_name=Linux', 'acpi_osi=')
        )
        self.assertEqual(inst.remove, tuple())
        self.assertEqual(inst.build_new_cmdline('quiet splash'),
            'quiet splash acpi_os_name=Linux acpi_osi='
        )


class Test_backlight_vendor(TestCase):
    def test_decribe(self):
        inst = actions.backlight_vendor()
        self.assertEqual(inst.describe(),
            'Enable brightness hot keys'
        )

    def test_build_new_cmdline(self):
        inst = actions.backlight_vendor()
        self.assertEqual(inst.add,
            ('acpi_backlight=vendor',)
        )
        self.assertEqual(inst.remove, tuple())
        self.assertEqual(inst.build_new_cmdline('quiet splash'),
            'quiet splash acpi_backlight=vendor'
        )


class Test_remove_backlight_vendor(TestCase):
    def test_decribe(self):
        inst = actions.remove_backlight_vendor()
        self.assertEqual(inst.describe(),
            'Remove brightness hot-key fix'
        )

    def test_build_new_cmdline(self):
        inst = actions.remove_backlight_vendor()
        self.assertEqual(inst.add, tuple())
        self.assertEqual(inst.remove,
            ('acpi_backlight=vendor',)
        )
        self.assertEqual(
            inst.build_new_cmdline('acpi_backlight=vendor quiet splash'),
            'quiet splash'
        )


class Test_radeon_dpm(TestCase):
    def test_describe(self):
        inst = actions.radeon_dpm()
        self.assertEqual(inst.describe(),
            'Enable Radeon GPU power management'
        )

    def test_build_new_cmdline(self):
        inst = actions.radeon_dpm()
        self.assertEqual(inst.add,
            ('radeon.dpm=1',)
        )
        self.assertEqual(inst.remove, tuple())
        self.assertEqual(inst.build_new_cmdline('quiet splash'),
            'quiet splash radeon.dpm=1'
        )


class Test_disable_power_well(TestCase):
    def test_describe(self):
        inst = actions.disable_power_well()
        self.assertEqual(inst.describe(),
            'Fix HDMI audio playback speed'
        )

    def test_build_new_cmdline(self):
        inst = actions.disable_power_well()
        self.assertEqual(inst.add,
            ('i915.disable_power_well=0',)
        )
        self.assertEqual(inst.remove, tuple())
        self.assertEqual(inst.build_new_cmdline('quiet splash'),
            'quiet splash i915.disable_power_well=0'
        )


class Test_plymouth1080(TestCase):
    def test_init(self):
        inst = actions.plymouth1080()
        self.assertIs(inst.update_grub, True)
        self.assertEqual(inst.filename, '/etc/default/grub')
        self.assertEqual(inst.value, 'GRUB_GFXPAYLOAD_LINUX="1920x1080"')

        tmp = TempDir()
        self.assertIs(inst.update_grub, True)
        inst = actions.plymouth1080(etcdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.join('default', 'grub'))
        self.assertEqual(inst.value, 'GRUB_GFXPAYLOAD_LINUX="1920x1080"')

    def test_describe(self):
        inst = actions.plymouth1080()
        self.assertEqual(inst.describe(),
            'Correctly diplay Ubuntu logo on boot'
        )

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.plymouth1080(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), True)
        open(inst.filename, 'a').write('\nGRUB_GFXPAYLOAD_LINUX="1920x1080"')
        self.assertIs(inst.get_isneeded(), False)

    def test_perform(self):
        SubProcess.reset(mocking=True)
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.plymouth1080(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)

        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(
            open(inst.filename, 'r').read(),
            GRUB_ORIG + '\nGRUB_GFXPAYLOAD_LINUX="1920x1080"'
        )
        self.assertEqual(inst.bak, actions.backup_filename(inst.filename))
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)

        open(inst.filename, 'w').write(
            'GRUB_GFXPAYLOAD_LINUX="foo bar"\n' + GRUB_ORIG
        )
        self.assertIsNone(inst.perform())
        self.assertEqual(
            open(inst.filename, 'r').read(),
            GRUB_ORIG + '\nGRUB_GFXPAYLOAD_LINUX="1920x1080"'
        )

        self.assertIsNone(inst.perform())
        self.assertEqual(
            open(inst.filename, 'r').read(),
            GRUB_ORIG + '\nGRUB_GFXPAYLOAD_LINUX="1920x1080"'
        )

        self.assertEqual(SubProcess.calls, [])


class Test_gfxpayload_text(TestCase):
    def test_init(self):
        inst = actions.gfxpayload_text()
        self.assertIs(inst.update_grub, True)
        self.assertEqual(inst.filename, '/etc/default/grub')
        self.assertEqual(inst.comment, '# Added by system76-driver:')
        self.assertEqual(inst.prefix, 'GRUB_GFXPAYLOAD_LINUX=')
        self.assertEqual(inst.value, 'GRUB_GFXPAYLOAD_LINUX=text')
        self.assertTrue(inst.value.startswith(inst.prefix))

        tmp = TempDir()
        self.assertIs(inst.update_grub, True)
        inst = actions.gfxpayload_text(etcdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.join('default', 'grub'))
        self.assertEqual(inst.comment, '# Added by system76-driver:')
        self.assertEqual(inst.value, 'GRUB_GFXPAYLOAD_LINUX=text')
        self.assertEqual(inst.prefix, 'GRUB_GFXPAYLOAD_LINUX=')
        self.assertTrue(inst.value.startswith(inst.prefix))

    def test_describe(self):
        inst = actions.gfxpayload_text()
        self.assertEqual(inst.describe(), 'Improve graphics UX for UEFI resume')

    def test_get_isneeded(self):
        SubProcess.reset(mocking=True)
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.gfxpayload_text(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'x').write(GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), True)
        open(inst.filename, 'a').write('\nGRUB_GFXPAYLOAD_LINUX=text')
        self.assertIs(inst.get_isneeded(), False)
        open(inst.filename, 'w').write('GRUB_GFXPAYLOAD_LINUX=text\n' + GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), False)

        # Correct GRUB_GFXPAYLOAD_LINUX=text line, all lines in random order:
        lines = GRUB_ORIG.splitlines()
        lines.append('GRUB_GFXPAYLOAD_LINUX=text')
        for i in range(100):
            random.shuffle(lines)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                open(inst.filename, 'w').write(content)
                self.assertIs(inst.get_isneeded(), False)
                self.assertEqual(tmp.listdir(), ['default'])
                self.assertEqual(tmp.listdir('default'), ['grub'])
                self.assertEqual(SubProcess.calls, [])

    def test_perform(self):
        def join(*parts):
            return '\n'.join(parts) + '\n'

        SubProcess.reset(mocking=True)
        COMMENT = '# Added by system76-driver:'
        VALUE = 'GRUB_GFXPAYLOAD_LINUX=text'
        EXPECTED = join(GRUB_ORIG, '', COMMENT, VALUE)

        # /etc/default/grub file is missing:
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.gfxpayload_text(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)
        self.assertEqual(tmp.listdir('default'), [])
        self.assertEqual(SubProcess.calls, [])

        # Original /etc/default/grub file:
        open(inst.filename, 'x').write(GRUB_ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), EXPECTED)
        self.assertEqual(inst.bak, actions.backup_filename(inst.filename))
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)
        self.assertEqual(tmp.listdir('default'),
            ['grub', path.basename(inst.bak)]
        )
        self.assertEqual(SubProcess.calls, [])

        # Some sanity check permutations:
        old = GRUB_ORIG + '\n' + VALUE  # What system76-driver used to do
        extra_space = GRUB_ORIG + '\n\n' + VALUE
        permutations = (
            old,
            old + '\n',
            old + '\n\n',
            extra_space,
            extra_space + '\n',
            extra_space + '\n\n',
            EXPECTED,  # Test round-trip
            EXPECTED + '\n',
            EXPECTED[:-1],
        )
        for content in permutations:
            tmp = TempDir()
            tmp.mkdir('default')
            inst = actions.gfxpayload_text(etcdir=tmp.dir)
            open(inst.filename, 'x').write(content)
            self.assertIsNone(inst.perform())
            self.assertEqual(open(inst.filename, 'r').read(), EXPECTED)
            self.assertEqual(inst.bak,
                actions.backup_filename(inst.filename)
            )
            self.assertEqual(open(inst.bak, 'r').read(), content)
            self.assertEqual(tmp.listdir('default'),
                ['grub', path.basename(inst.bak)]
            )
            self.assertEqual(SubProcess.calls, [])

        # Existing GRUB_GFXPAYLOAD_LINUX or COMMENT line at a random position:
        orig_lines = tuple(GRUB_ORIG.splitlines())
        extra_lines = (
            COMMENT,
            VALUE,
            ' ' + COMMENT,
            ' ' + VALUE,
            ' ' + COMMENT + ' ',
            ' ' + VALUE + ' ',
            'GRUB_GFXPAYLOAD_LINUX=foobar',
            'GRUB_GFXPAYLOAD_LINUX=',
        )
        for extra in extra_lines:
            lines = list(orig_lines)
            index = random.randint(0, len(lines))
            lines.insert(index, extra)
            self.assertEqual(len(lines), len(orig_lines) + 1)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                self.assertNotEqual(content, EXPECTED)
                tmp = TempDir()
                tmp.mkdir('default')
                inst = actions.gfxpayload_text(etcdir=tmp.dir)
                open(inst.filename, 'x').write(content)
                self.assertIsNone(inst.perform())
                self.assertEqual(open(inst.filename, 'r').read(), EXPECTED)
                self.assertEqual(inst.bak,
                    actions.backup_filename(inst.filename)
                )
                self.assertEqual(open(inst.bak, 'r').read(), content)
                self.assertEqual(tmp.listdir('default'),
                    ['grub', path.basename(inst.bak)]
                )
                self.assertEqual(SubProcess.calls, [])

        # Multiple existing GRUB_GFXPAYLOAD_LINUX and COMMENT lines at random
        # positions:
        for i in range(100):
            lines = list(orig_lines)
            for extra in extra_lines:
                index = random.randint(0, len(lines))
                lines.insert(index, extra)
            self.assertEqual(len(lines), len(orig_lines) + 8)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                self.assertNotEqual(content, EXPECTED)
                tmp = TempDir()
                tmp.mkdir('default')
                inst = actions.gfxpayload_text(etcdir=tmp.dir)
                open(inst.filename, 'x').write(content)
                self.assertIsNone(inst.perform())
                self.assertEqual(open(inst.filename, 'r').read(), EXPECTED)
                self.assertEqual(inst.bak,
                    actions.backup_filename(inst.filename)
                )
                self.assertEqual(open(inst.bak, 'r').read(), content)
                self.assertEqual(tmp.listdir('default'),
                    ['grub', path.basename(inst.bak)]
                )
                self.assertEqual(SubProcess.calls, [])

        # GRUB_ORIG lines in random order:
        lines = list(orig_lines)
        for i in range(100):
            random.shuffle(lines)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            new = join(content1.rstrip(), '', COMMENT, VALUE)
            self.assertNotEqual(new, GRUB_ORIG)
            for content in (content1, content2):
                tmp = TempDir()
                tmp.mkdir('default')
                inst = actions.gfxpayload_text(etcdir=tmp.dir)
                open(inst.filename, 'x').write(content)
                self.assertIsNone(inst.perform())
                self.assertEqual(open(inst.filename, 'r').read(), new)
                self.assertEqual(inst.bak,
                    actions.backup_filename(inst.filename)
                )
                self.assertEqual(open(inst.bak, 'r').read(), content)
                self.assertEqual(tmp.listdir('default'),
                    ['grub', path.basename(inst.bak)]
                )
                self.assertEqual(SubProcess.calls, [])

        # EXPECTED lines in random order:
        for i in range(100):
            lines = EXPECTED.split('\n')
            random.shuffle(lines)
            content = join(*lines)
            lines.remove(COMMENT)
            lines.remove(VALUE)
            while lines and lines[-1] == '':
                lines.pop()
            lines.extend(['', COMMENT, VALUE])
            new = join(*lines)
            tmp = TempDir()
            tmp.mkdir('default')
            inst = actions.gfxpayload_text(etcdir=tmp.dir)
            open(inst.filename, 'x').write(content)
            self.assertIsNone(inst.perform())
            self.assertEqual(open(inst.filename, 'r').read(), new)
            self.assertEqual(inst.bak,
                actions.backup_filename(inst.filename)
            )
            self.assertEqual(open(inst.bak, 'r').read(), content)
            self.assertEqual(tmp.listdir('default'),
                ['grub', path.basename(inst.bak)]
            )
            self.assertEqual(SubProcess.calls, [])

        # /etc/default/grub is empty or contains only white-space:
        expected = join('', COMMENT, VALUE)
        empty_content = (
            '',
            '\n',
            ' ',
            ' \n',
            '\t',
            '\t\n',
            '\n'.join([' ', '\t', '  \t ']),
            '\n'.join([' ', '\t', '  \t ', '']),
        )
        for content in empty_content:
            tmp = TempDir()
            tmp.mkdir('default')
            inst = actions.gfxpayload_text(etcdir=tmp.dir)
            open(inst.filename, 'x').write(content)
            self.assertIsNone(inst.perform())
            self.assertEqual(open(inst.filename, 'r').read(), expected)
            self.assertEqual(inst.bak,
                actions.backup_filename(inst.filename)
            )
            self.assertEqual(open(inst.bak, 'r').read(), content)
            self.assertEqual(tmp.listdir('default'),
                ['grub', path.basename(inst.bak)]
            )
            self.assertEqual(SubProcess.calls, [])


class Test_remove_gfxpayload_text(TestCase):
    def test_init(self):
        inst = actions.remove_gfxpayload_text()
        self.assertIs(inst.update_grub, True)
        self.assertEqual(inst.filename, '/etc/default/grub')
        self.assertEqual(inst.comment, '# Added by system76-driver:')
        self.assertEqual(inst.prefix, 'GRUB_GFXPAYLOAD_LINUX=')
        self.assertEqual(inst.value, 'GRUB_GFXPAYLOAD_LINUX=text')
        self.assertTrue(inst.value.startswith(inst.prefix))

        tmp = TempDir()
        self.assertIs(inst.update_grub, True)
        inst = actions.remove_gfxpayload_text(etcdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.join('default', 'grub'))
        self.assertEqual(inst.comment, '# Added by system76-driver:')
        self.assertEqual(inst.value, 'GRUB_GFXPAYLOAD_LINUX=text')
        self.assertEqual(inst.prefix, 'GRUB_GFXPAYLOAD_LINUX=')
        self.assertTrue(inst.value.startswith(inst.prefix))

    def test_describe(self):
        inst = actions.remove_gfxpayload_text()
        self.assertEqual(inst.describe(), 'Remove GRUB_GFXPAYLOAD_LINUX=text line')

    def test_get_isneeded(self):
        SubProcess.reset(mocking=True)
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.remove_gfxpayload_text(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'x').write(GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), False)

        comment = '# Added by system76-driver:'
        value = 'GRUB_GFXPAYLOAD_LINUX=text'
        end = '\n'.join(['', comment, value, ''])

        for text in [comment, value, end]:
            open(inst.filename, 'w').write(text)
            self.assertIs(inst.get_isneeded(), True)
            open(inst.filename, 'w').write('\n'.join([GRUB_ORIG, text]))
            self.assertIs(inst.get_isneeded(), True)
            open(inst.filename, 'w').write('\n'.join([text, GRUB_ORIG]))
            self.assertIs(inst.get_isneeded(), True)
            self.assertEqual(tmp.listdir(), ['default'])
            self.assertEqual(tmp.listdir('default'), ['grub'])
            self.assertEqual(SubProcess.calls, [])

        # Lines in random order, no action needed:
        lines = GRUB_ORIG.splitlines()
        for i in range(50):
            random.shuffle(lines)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                open(inst.filename, 'w').write(content)
                self.assertIs(inst.get_isneeded(), False)
                self.assertEqual(tmp.listdir(), ['default'])
                self.assertEqual(tmp.listdir('default'), ['grub'])
                self.assertEqual(SubProcess.calls, [])

        # Lines in random order, contains comment line:
        lines = '\n'.join([GRUB_ORIG, comment]).splitlines()
        for i in range(50):
            random.shuffle(lines)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                open(inst.filename, 'w').write(content)
                self.assertIs(inst.get_isneeded(), True)
                self.assertEqual(tmp.listdir(), ['default'])
                self.assertEqual(tmp.listdir('default'), ['grub'])
                self.assertEqual(SubProcess.calls, [])

        # Lines in random order, contains value line:
        lines = '\n'.join([GRUB_ORIG, value]).splitlines()
        for i in range(50):
            random.shuffle(lines)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                open(inst.filename, 'w').write(content)
                self.assertIs(inst.get_isneeded(), True)
                self.assertEqual(tmp.listdir(), ['default'])
                self.assertEqual(tmp.listdir('default'), ['grub'])
                self.assertEqual(SubProcess.calls, [])

        # Lines in random order, contains comment line and value line:
        lines = (GRUB_ORIG + end).splitlines()
        for i in range(50):
            random.shuffle(lines)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                open(inst.filename, 'w').write(content)
                self.assertIs(inst.get_isneeded(), True)
                self.assertEqual(tmp.listdir(), ['default'])
                self.assertEqual(tmp.listdir('default'), ['grub'])
                self.assertEqual(SubProcess.calls, [])

    def test_perform(self):
        def join(*parts):
            return '\n'.join(parts) + '\n'

        SubProcess.reset(mocking=True)
        COMMENT = '# Added by system76-driver:'
        VALUE = 'GRUB_GFXPAYLOAD_LINUX=text'
        ORIG = join(GRUB_ORIG)
        MODIFIED = join(GRUB_ORIG, '', COMMENT, VALUE)

        # /etc/default/grub file is missing:
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.remove_gfxpayload_text(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)
        self.assertEqual(tmp.listdir('default'), [])
        self.assertEqual(SubProcess.calls, [])

        # Original /etc/default/grub file:
        open(inst.filename, 'x').write(ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), ORIG)
        self.assertEqual(inst.bak, actions.backup_filename(inst.filename))
        self.assertEqual(open(inst.bak, 'r').read(), ORIG)
        self.assertEqual(tmp.listdir('default'),
            ['grub', path.basename(inst.bak)]
        )
        self.assertEqual(SubProcess.calls, [])

        # Some sanity check permutations:
        old = ORIG + VALUE  # What system76-driver used to do
        extra_space = ORIG + '\n' + VALUE
        permutations = (
            old,
            old + '\n',
            old + '\n\n',
            extra_space,
            extra_space + '\n',
            extra_space + '\n\n',
            MODIFIED,  # Test round-trip
            MODIFIED + '\n',
            MODIFIED[:-1],
        )
        for content in permutations:
            tmp = TempDir()
            tmp.mkdir('default')
            inst = actions.remove_gfxpayload_text(etcdir=tmp.dir)
            open(inst.filename, 'x').write(content)
            self.assertIsNone(inst.perform())
            self.assertEqual(open(inst.filename, 'r').read(), ORIG)
            self.assertEqual(inst.bak,
                actions.backup_filename(inst.filename)
            )
            self.assertEqual(open(inst.bak, 'r').read(), content)
            self.assertEqual(tmp.listdir('default'),
                ['grub', path.basename(inst.bak)]
            )
            self.assertEqual(SubProcess.calls, [])

        # Existing GRUB_GFXPAYLOAD_LINUX or COMMENT line at a random position:
        orig_lines = tuple(ORIG.splitlines())
        extra_lines = (
            COMMENT,
            VALUE,
            ' ' + COMMENT,
            ' ' + VALUE,
            COMMENT + ' ',
            VALUE + ' ',
            ' ' + COMMENT + ' ',
            ' ' + VALUE + ' ',
        )
        for extra in extra_lines:
            lines = list(orig_lines)
            index = random.randint(0, len(lines))
            lines.insert(index, extra)
            self.assertEqual(len(lines), len(orig_lines) + 1)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                self.assertNotEqual(content, ORIG)
                tmp = TempDir()
                tmp.mkdir('default')
                inst = actions.remove_gfxpayload_text(etcdir=tmp.dir)
                open(inst.filename, 'x').write(content)
                self.assertIsNone(inst.perform())
                self.assertEqual(open(inst.filename, 'r').read(), ORIG)
                self.assertEqual(inst.bak,
                    actions.backup_filename(inst.filename)
                )
                self.assertEqual(open(inst.bak, 'r').read(), content)
                self.assertEqual(tmp.listdir('default'),
                    ['grub', path.basename(inst.bak)]
                )
                self.assertEqual(SubProcess.calls, [])

        # Multiple existing GRUB_GFXPAYLOAD_LINUX and COMMENT lines at random
        # positions:
        for i in range(100):
            lines = list(orig_lines)
            for extra in extra_lines:
                index = random.randint(0, len(lines))
                lines.insert(index, extra)
            self.assertEqual(len(lines), len(orig_lines) + 8)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            for content in (content1, content2):
                self.assertNotEqual(content, ORIG)
                tmp = TempDir()
                tmp.mkdir('default')
                inst = actions.remove_gfxpayload_text(etcdir=tmp.dir)
                open(inst.filename, 'x').write(content)
                self.assertIsNone(inst.perform())
                self.assertEqual(open(inst.filename, 'r').read(), ORIG)
                self.assertEqual(inst.bak,
                    actions.backup_filename(inst.filename)
                )
                self.assertEqual(open(inst.bak, 'r').read(), content)
                self.assertEqual(tmp.listdir('default'),
                    ['grub', path.basename(inst.bak)]
                )
                self.assertEqual(SubProcess.calls, [])

        # ORIG lines in random order:
        for i in range(100):
            lines = list(orig_lines)
            random.shuffle(lines)
            content1 = '\n'.join(lines)  # Without final '\n'
            content2 = content1 + '\n'   # With final '\n'
            expected = content1.rstrip() + '\n'
            self.assertNotEqual(expected, ORIG)
            for content in (content1, content2):
                tmp = TempDir()
                tmp.mkdir('default')
                inst = actions.remove_gfxpayload_text(etcdir=tmp.dir)
                open(inst.filename, 'x').write(content)
                self.assertIsNone(inst.perform())
                self.assertEqual(open(inst.filename, 'r').read(), expected)
                self.assertEqual(inst.bak,
                    actions.backup_filename(inst.filename)
                )
                self.assertEqual(open(inst.bak, 'r').read(), content)
                self.assertEqual(tmp.listdir('default'),
                    ['grub', path.basename(inst.bak)]
                )
                self.assertEqual(SubProcess.calls, [])
            # Use same random order of orig lines, but add lines that should be
            # removed at random indexes:
            for extra in extra_lines:
                index = random.randint(0, len(lines))
                lines.insert(index, extra)
                content1 = '\n'.join(lines)  # Without final '\n'
                content2 = content1 + '\n'   # With final '\n'
                for content in (content1, content2):
                    tmp = TempDir()
                    tmp.mkdir('default')
                    inst = actions.remove_gfxpayload_text(etcdir=tmp.dir)
                    open(inst.filename, 'x').write(content)
                    self.assertIsNone(inst.perform())
                    self.assertEqual(open(inst.filename, 'r').read(), expected)
                    self.assertEqual(inst.bak,
                        actions.backup_filename(inst.filename)
                    )
                    self.assertEqual(open(inst.bak, 'r').read(), content)
                    self.assertEqual(tmp.listdir('default'),
                        ['grub', path.basename(inst.bak)]
                    )
                    self.assertEqual(SubProcess.calls, [])


class Test_uvcquirks(TestCase):
    def test_init(self):
        inst = actions.uvcquirks()
        self.assertEqual(inst.filename, '/etc/modprobe.d/uvc.conf')

        tmp = TempDir()
        inst = actions.uvcquirks(rootdir=tmp.dir)
        self.assertEqual(inst.filename,
            tmp.join('etc', 'modprobe.d', 'uvc.conf')
        )

    def test_read(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'modprobe.d')
        inst = actions.uvcquirks(rootdir=tmp.dir)
        self.assertIsNone(inst.read())
        tmp.write(b'Hello, World', 'etc', 'modprobe.d', 'uvc.conf')
        self.assertEqual(inst.read(), 'Hello, World')

    def test_describe(self):
        inst = actions.uvcquirks()
        self.assertEqual(inst.describe(), 'Webcam quirk fixes')

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'modprobe.d')
        inst = actions.uvcquirks(rootdir=tmp.dir)

        # Missing file
        self.assertIs(inst.get_isneeded(), True)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), True)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(inst.content)
        os.chmod(inst.filename, 0o666)
        self.assertIs(inst.get_isneeded(), True)
        os.chmod(inst.filename, 0o600)
        self.assertIs(inst.get_isneeded(), True)

        # All good:
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), False)

    def _check_file(self, inst):
        self.assertEqual(open(inst.filename, 'r').read(), inst.content)
        st = os.stat(inst.filename)
        self.assertEqual(stat.S_IMODE(st.st_mode), 0o644)

    def test_perform(self):
        tmp = TempDir()
        inst = actions.uvcquirks(rootdir=tmp.dir)

        # Missing directories
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Missing file
        tmp.remove(inst.filename)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o644)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(inst.content)
        os.chmod(inst.filename, 0o666)
        self.assertIsNone(inst.perform())
        self._check_file(inst)
        os.chmod(inst.filename, 0o600)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Action didn't need to be performed:
        self.assertIsNone(inst.perform())
        self._check_file(inst)


class Test_internal_mic_gain(TestCase):
    def test_init(self):
        inst = actions.internal_mic_gain()
        self.assertEqual(inst.filename,
            '/usr/share/pulseaudio/alsa-mixer/paths/analog-input-internal-mic.conf'
        )

        tmp = TempDir()
        inst = actions.internal_mic_gain(rootdir=tmp.dir)
        self.assertEqual(inst.filename,
            tmp.join(
                'usr',
                'share',
                'pulseaudio',
                'alsa-mixer',
                'paths',
                'analog-input-internal-mic.conf'
            )
        )

    def test_read(self):
        tmp = TempDir()
        tmp.makedirs('usr', 'share', 'pulseaudio', 'alsa-mixer', 'paths')
        inst = actions.internal_mic_gain(rootdir=tmp.dir)
        self.assertIsNone(inst.read())
        tmp.write(b'Hello, World', 'usr', 'share', 'pulseaudio', 'alsa-mixer',
                'paths', 'analog-input-internal-mic.conf')
        self.assertEqual(inst.read(), 'Hello, World')

    def test_describe(self):
        inst = actions.internal_mic_gain()
        self.assertEqual(inst.describe(), 'Fix Internal Mic Gain')

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.makedirs('usr', 'share', 'pulseaudio', 'alsa-mixer', 'paths')
        inst = actions.internal_mic_gain(rootdir=tmp.dir)

        # Missing file
        self.assertIs(inst.get_isneeded(), True)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), True)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(inst.content)
        os.chmod(inst.filename, 0o666)
        self.assertIs(inst.get_isneeded(), True)
        os.chmod(inst.filename, 0o600)
        self.assertIs(inst.get_isneeded(), True)

        # All good:
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.get_isneeded(), False)

    def _check_file(self, inst):
        self.assertEqual(open(inst.filename, 'r').read(), inst.content)
        st = os.stat(inst.filename)
        self.assertEqual(stat.S_IMODE(st.st_mode), 0o644)

    def test_perform(self):
        tmp = TempDir()
        inst = actions.internal_mic_gain(rootdir=tmp.dir)

        # Missing directories
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Missing file
        tmp.remove(inst.filename)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o644)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(inst.content)
        os.chmod(inst.filename, 0o666)
        self.assertIsNone(inst.perform())
        self._check_file(inst)
        os.chmod(inst.filename, 0o600)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Action didn't need to be performed:
        self.assertIsNone(inst.perform())
        self._check_file(inst)


PATCH_CONTENT = """[codec]
0x00000000 0x00000000 0

[verb]
0x1b 0x707 0x0004
"""


class Test_dac_fixup(TestCase):
    def setUp(self):
        self.tmp = TempDir()
        self.tmp.makedirs('sys', 'class', 'sound', 'hwC0D0')
        self.tmp.makedirs('lib', 'firmware')
        self.tmp.makedirs('etc', 'modprobe.d')
        self.vendor_id = random.randint(0, 0xffffffff)
        self.subsystem_id = random.randint(0, 0xffffffff)
        for name in ('vendor_id', 'subsystem_id'):
            value = getattr(self, name)
            content = '0x{:08x}\n'.format(value).encode()
            self.tmp.write(content, 'sys', 'class', 'sound', 'hwC0D0', name)
        self.patch_content = actions.DAC_PATCH.format(
            vendor_id=self.vendor_id, subsystem_id=self.subsystem_id
        )

    def tearDown(self):
        self.tmp = None
        self.vendor_id = None
        self.subsystem_id = None

    def test_init(self):
        inst = actions.dac_fixup(rootdir=self.tmp.dir)
        self.assertEqual(inst.filename1,
            self.tmp.join('lib', 'firmware', 'system76-audio-patch')
        )
        self.assertEqual(inst.filename2,
            self.tmp.join('etc', 'modprobe.d', 'system76-alsa-base.conf')
        )
        self.assertEqual(inst.content1, self.patch_content)
        self.assertEqual(inst.content2, actions.DAC_MODPROBE)

    def test_read1(self):
        inst = actions.dac_fixup(rootdir=self.tmp.dir)

        # No file:
        self.assertIsNone(inst.read1())

        # File exists:
        marker = actions.random_id()
        with open(inst.filename1, 'x') as fp:
            fp.write(marker)
        self.assertEqual(inst.read1(), marker)

    def test_read2(self):
        inst = actions.dac_fixup(rootdir=self.tmp.dir)

        # No file:
        self.assertIsNone(inst.read2())

        # File exists:
        marker = actions.random_id()
        with open(inst.filename2, 'x') as fp:
            fp.write(marker)
        self.assertEqual(inst.read2(), marker)

    def test_get_isneeded(self):
        inst = actions.dac_fixup(rootdir=self.tmp.dir)

        # filename1, filename2 both missing:
        self.assertIs(inst.get_isneeded(), True)

        # filename1, filename2 both exist and have correct content:
        with open(inst.filename1, 'x') as fp:
            fp.write(inst.content1)
        with open(inst.filename2, 'x') as fp:
            fp.write(inst.content2)
        self.assertIs(inst.get_isneeded(), False)

        # filename1 has wrong content:
        with open(inst.filename1, 'w') as fp:
            fp.write(inst.content2)
        self.assertIs(inst.get_isneeded(), True)

        # filename1 is missing:
        os.remove(inst.filename1)
        self.assertIs(inst.get_isneeded(), True)

        # Put filename1 back in correct post-action state:
        with open(inst.filename1, 'x') as fp:
            fp.write(inst.content1)
        self.assertIs(inst.get_isneeded(), False)

        # filename2 has wrong content:
        with open(inst.filename2, 'w') as fp:
            fp.write(inst.content1)
        self.assertIs(inst.get_isneeded(), True)

        # filename2 is missing:
        os.remove(inst.filename2)
        self.assertIs(inst.get_isneeded(), True)

        # Put filename2 back in correct post-action state:
        with open(inst.filename2, 'x') as fp:
            fp.write(inst.content2)
        self.assertIs(inst.get_isneeded(), False)

    def test_perform(self):
        inst = actions.dac_fixup(rootdir=self.tmp.dir)
        self.assertIs(inst.get_isneeded(), True)
        self.assertIsNone(inst.perform())
        self.assertIs(inst.get_isneeded(), False)

    def test_describe(self):
        inst = actions.dac_fixup()
        self.assertEqual(inst.describe(), 'Enable high-quality audio DAC')
