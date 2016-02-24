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
import stat
from base64 import b32decode, b32encode

from .helpers import TempDir
from system76driver.mockable import SubProcess
from system76driver import actions


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
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.tmp)

        # Missing file:
        tmp.mkdir('some')
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
        self.assertEqual(inst.filename, '/etc/default/grub')
        self.assertEqual(inst.add, tuple())
        self.assertEqual(inst.remove, tuple())

        tmp = TempDir()
        inst = actions.GrubAction(etcdir=tmp.dir)
        self.assertIs(inst.update_grub, True)
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
            'hello world'
        )

        class Subclass(actions.GrubAction):
            add = ('nurse', 'naughty', 'hello')
            remove = ('other', 'world')

        inst = Subclass()
        self.assertEqual(
            inst.build_new_cmdline('world hello'),
            'hello naughty nurse'
        )
        self.assertEqual(
            inst.build_new_cmdline('naughty nurse hello'),
            'hello naughty nurse'
        )

    def test_iter_lines(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            list(inst.iter_lines())
        self.assertEqual(cm.exception.filename, inst.filename)

        open(inst.filename, 'x').write(GRUB_ORIG)
        self.assertEqual('\n'.join(inst.iter_lines()), GRUB_ORIG)
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)
        self.assertEqual(inst.bak, actions.backup_filename(inst.filename))

        open(inst.filename, 'w').write(
            GRUB.format('foo bar aye')
        )
        self.assertEqual(
            '\n'.join(inst.iter_lines()),
            GRUB.format('aye bar foo')
        )
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)

        # Test subclass with different GrubAction.cmdline:
        class Example(actions.GrubAction):
            add = ('acpi_os_name=Linux', 'acpi_osi=')

        tmp = TempDir()
        tmp.mkdir('default')
        inst = Example(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            list(inst.iter_lines())
        self.assertEqual(cm.exception.filename, inst.filename)

        open(inst.filename, 'x').write(GRUB_ORIG)
        self.assertEqual(
            '\n'.join(inst.iter_lines()),
            GRUB.format('acpi_os_name=Linux acpi_osi= quiet splash')
        )
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)
        self.assertEqual(inst.bak, actions.backup_filename(inst.filename))

        self.assertEqual(
            '\n'.join(inst.iter_lines()),
            GRUB.format('acpi_os_name=Linux acpi_osi= quiet splash')
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

        with open(inst.filename, 'x') as fp:
            fp.write(GRUB_ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), GRUB_ORIG)

        with open(inst.filename, 'w') as fp:
            fp.write(GRUB.format('c a b'))
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), GRUB.format('a b c'))

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

        with open(inst.filename, 'x') as fp:
            fp.write(GRUB_ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(
            open(inst.filename, 'r').read(),
            GRUB.format('bar foo quiet splash')
        )

        self.assertIsNone(inst.perform())
        self.assertEqual(
            open(inst.filename, 'r').read(),
            GRUB.format('bar foo quiet splash')
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
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.tmp)

        # Missing file
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'power.d')
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
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.tmp)

        # Missing file
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'power.d')
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
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.tmp)

        # Missing file
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'tmpfiles.d')
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
            'acpi_os_name=Linux acpi_osi= quiet splash'
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
            'acpi_backlight=vendor quiet splash'
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
            'quiet radeon.dpm=1 splash'
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
            'i915.disable_power_well=0 quiet splash'
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
        self.assertEqual(inst.value, 'GRUB_GFXPAYLOAD_LINUX=text')

        tmp = TempDir()
        self.assertIs(inst.update_grub, True)
        inst = actions.gfxpayload_text(etcdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.join('default', 'grub'))
        self.assertEqual(inst.value, 'GRUB_GFXPAYLOAD_LINUX=text')

    def test_describe(self):
        inst = actions.gfxpayload_text()
        self.assertEqual(inst.describe(), 'Fix resume in UEFI mode')

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.gfxpayload_text(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), True)
        open(inst.filename, 'a').write('\nGRUB_GFXPAYLOAD_LINUX=text')
        self.assertIs(inst.get_isneeded(), False)
        open(inst.filename, 'w').write('GRUB_GFXPAYLOAD_LINUX=text\n' + GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), False)

    def test_perform(self):
        SubProcess.reset(mocking=True)
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.gfxpayload_text(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)

        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(
            open(inst.filename, 'r').read(),
            GRUB_ORIG + '\nGRUB_GFXPAYLOAD_LINUX=text\n'
        )
        self.assertEqual(inst.bak, actions.backup_filename(inst.filename))
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)

        open(inst.filename, 'w').write(
            'GRUB_GFXPAYLOAD_LINUX=foobar\n' + GRUB_ORIG
        )
        self.assertIsNone(inst.perform())
        self.assertEqual(
            open(inst.filename, 'r').read(),
            GRUB_ORIG + '\nGRUB_GFXPAYLOAD_LINUX=text\n'
        )

        self.assertIsNone(inst.perform())
        self.assertEqual(
            open(inst.filename, 'r').read(),
            GRUB_ORIG + '\nGRUB_GFXPAYLOAD_LINUX=text\n'
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
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.tmp)

        # Missing file
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'modprobe.d')
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
            tmp.join('usr', 'share', 'pulseaudio', 'alsa-mixer', 'paths', 'analog-input-internal-mic.conf')
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
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.tmp)

        # Missing file
        tmp.makedirs('usr', 'share', 'pulseaudio', 'alsa-mixer', 'paths')
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
