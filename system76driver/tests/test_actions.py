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
Unit tests for `system76driver.actions` module.
"""

from unittest import TestCase
import os
import stat
from base64 import b32decode, b32encode

from .helpers import TempDir
from system76driver.mockable import SubProcess
from system76driver import actions


GRUB_ORIG = """
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.
# For full documentation of the options in this file, see:
#   info -f grub -n 'Simple configuration'

GRUB_DEFAULT=0
GRUB_HIDDEN_TIMEOUT=0
GRUB_HIDDEN_TIMEOUT_QUIET=true
GRUB_TIMEOUT=10
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
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

GRUB_MOD = """
# If you change this file, run 'update-grub' afterwards to update
# /boot/grub/grub.cfg.
# For full documentation of the options in this file, see:
#   info -f grub -n 'Simple configuration'

GRUB_DEFAULT=0
GRUB_HIDDEN_TIMEOUT=0
GRUB_HIDDEN_TIMEOUT_QUIET=true
GRUB_TIMEOUT=10
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash acpi_os_name=Linux acpi_osi="
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

    def test_run_actions(self):
        self.skipTest('FIXME')


class TestAction(TestCase):
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
        self.assertEqual(inst.cmdline, 'quiet splash')

        tmp = TempDir()
        inst = actions.GrubAction(etcdir=tmp.dir)
        self.assertIs(inst.update_grub, True)
        self.assertEqual(inst.filename, tmp.join('default', 'grub'))
        self.assertEqual(inst.cmdline, 'quiet splash')

    def test_read(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.read()
        self.assertEqual(cm.exception.filename, inst.filename)
        tmp.write(b'foobar\n', 'default', 'grub')
        self.assertEqual(inst.read(), 'foobar\n')

    def test_get_cmdline(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)

        # Missing file:
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_cmdline()
        self.assertEqual(cm.exception.filename, inst.filename)

        # Bad content:
        open(inst.filename, 'x').write('wont work\n')
        with self.assertRaises(Exception) as cm:
            inst.get_cmdline()
        self.assertEqual(str(cm.exception),
            'Could not parse GRUB_CMDLINE_LINUX_DEFAULT'
        )

        # Good content:
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertEqual(inst.get_cmdline(), 'quiet splash')
        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertEqual(inst.get_cmdline(),
            'quiet splash acpi_os_name=Linux acpi_osi='
        )

    def test_iter_lines(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            list(inst.iter_lines())
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertEqual('\n'.join(inst.iter_lines()), GRUB_ORIG)
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)
        self.assertEqual(inst.bak, actions.backup_filename(inst.filename))

        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertEqual('\n'.join(inst.iter_lines()), GRUB_ORIG)
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)

        # Test subclass with different GrubAction.cmdline:
        class Example(actions.GrubAction):
            extra = ('acpi_os_name=Linux', 'acpi_osi=')

        tmp = TempDir()
        tmp.mkdir('default')
        inst = Example(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            list(inst.iter_lines())
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertEqual('\n'.join(inst.iter_lines()), GRUB_MOD)
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)
        self.assertEqual(inst.bak, actions.backup_filename(inst.filename))

        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertEqual('\n'.join(inst.iter_lines()), GRUB_MOD)
        self.assertEqual(open(inst.bak, 'r').read(), GRUB_ORIG)

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), False)
        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertIs(inst.get_isneeded(), True)

        # Test subclass with different GrubAction.cmdline:
        class Example(actions.GrubAction):
            extra = ('acpi_os_name=Linux', 'acpi_osi=')

        tmp = TempDir()
        tmp.mkdir('default')
        inst = Example(etcdir=tmp.dir)
        self.assertEqual(inst.cmdline,
            'quiet splash acpi_os_name=Linux acpi_osi='
        )
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), True)
        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertIs(inst.get_isneeded(), False)

    def test_perform(self):
        SubProcess.reset(mocking=True)

        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.GrubAction(etcdir=tmp.dir)

        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)

        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), GRUB_ORIG)

        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), GRUB_ORIG)

        self.assertEqual(SubProcess.calls, [])

        # Test subclass with different GrubAction.cmdline:
        class Example(actions.GrubAction):
            extra = ('acpi_os_name=Linux', 'acpi_osi=')

        tmp = TempDir()
        tmp.mkdir('default')
        inst = Example(etcdir=tmp.dir)

        self.assertEqual(inst.cmdline,
            'quiet splash acpi_os_name=Linux acpi_osi='
        )
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)

        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), GRUB_MOD)

        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), GRUB_MOD)

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


class Test_lemu1(TestCase):
    def test_init(self):
        inst = actions.lemu1()
        self.assertEqual(inst.filename, '/etc/default/grub')
        self.assertEqual(inst.cmdline,
            'quiet splash acpi_os_name=Linux acpi_osi='
        )
        tmp = TempDir()
        inst = actions.lemu1(etcdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.join('default', 'grub'))
        self.assertEqual(inst.cmdline,
            'quiet splash acpi_os_name=Linux acpi_osi='
        )

    def test_decribe(self):
        inst = actions.lemu1()
        self.assertEqual(inst.describe(),
            'Enable brightness hot keys'
        )

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.lemu1(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.get_isneeded()
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIs(inst.get_isneeded(), True)
        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertIs(inst.get_isneeded(), False)

    def test_perform(self):
        tmp = TempDir()
        tmp.mkdir('default')
        inst = actions.lemu1(etcdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)
        open(inst.filename, 'w').write(GRUB_ORIG)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), GRUB_MOD)
        open(inst.filename, 'w').write(GRUB_MOD)
        self.assertIsNone(inst.perform())
        self.assertEqual(open(inst.filename, 'r').read(), GRUB_MOD)


class Test_backlight_vendor(TestCase):
    def test_init(self):
        inst = actions.backlight_vendor()
        self.assertEqual(inst.filename, '/etc/default/grub')
        self.assertEqual(inst.cmdline, 'quiet splash acpi_backlight=vendor')
        tmp = TempDir()
        inst = actions.backlight_vendor(etcdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.join('default', 'grub'))
        self.assertEqual(inst.cmdline, 'quiet splash acpi_backlight=vendor')

    def test_decribe(self):
        inst = actions.backlight_vendor()
        self.assertEqual(inst.describe(), 'Enable brightness hot keys')


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


class Test_sata_alpm(TestCase):
    def test_init(self):
        inst = actions.sata_alpm()
        self.assertEqual(inst.filename, '/etc/pm/config.d/sata_alpm')
        tmp = TempDir()
        inst = actions.sata_alpm(rootdir=tmp.dir)
        self.assertEqual(inst.filename,
            tmp.join('etc', 'pm', 'config.d', 'sata_alpm')
        )

    def test_read(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'config.d')
        inst = actions.sata_alpm(rootdir=tmp.dir)
        self.assertIsNone(inst.read())
        tmp.write(b'Hello, World', 'etc', 'pm', 'config.d', 'sata_alpm')
        self.assertEqual(inst.read(), 'Hello, World')

    def test_describe(self):
        inst = actions.sata_alpm()
        self.assertEqual(inst.describe(),
            'Enable SATA Link Power Management (ALPM)')

    def test_get_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'config.d')
        inst = actions.sata_alpm(rootdir=tmp.dir)

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
        inst = actions.sata_alpm(rootdir=tmp.dir)

        # Missing directories
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.tmp)

        # Missing file
        tmp.mkdir('etc')
        tmp.mkdir('etc', 'pm')
        tmp.mkdir('etc', 'pm', 'config.d')
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

