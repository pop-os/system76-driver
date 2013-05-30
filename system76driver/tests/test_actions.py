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

from .helpers import TempDir
from system76driver import actions


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

    def test_isneeded(self):
        a = actions.Action()
        with self.assertRaises(NotImplementedError) as cm:
            a.isneeded()
        self.assertEqual(str(cm.exception), 'Action.isneeded()')

        class Example(actions.Action):
            pass

        a = Example()
        with self.assertRaises(NotImplementedError) as cm:
            a.isneeded()
        self.assertEqual(str(cm.exception), 'Example.isneeded()')

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


class Test_wifi_pm_disable(TestCase):
    def test_init(self):
        inst = actions.wifi_pm_disable()
        self.assertEqual(inst.filename, '/etc/pm/power.d/wireless')

        tmp = TempDir()
        inst = actions.wifi_pm_disable(etcdir=tmp.dir)
        self.assertEqual(inst.filename, tmp.join('pm', 'power.d', 'wireless'))

    def test_read(self):
        tmp = TempDir()
        tmp.mkdir('pm')
        tmp.mkdir('pm', 'power.d')
        inst = actions.wifi_pm_disable(etcdir=tmp.dir)
        self.assertIsNone(inst.read())
        tmp.write(b'Hello, World', 'pm', 'power.d', 'wireless')
        self.assertEqual(inst.read(), 'Hello, World')

    def test_describe(self):
        inst = actions.wifi_pm_disable()
        self.assertEqual(inst.describe(), 'Improve WiFi performance on Battery')

    def test_isneeded(self):
        tmp = TempDir()
        tmp.mkdir('pm')
        tmp.mkdir('pm', 'power.d')
        inst = actions.wifi_pm_disable(etcdir=tmp.dir)

        # Missing file
        self.assertIs(inst.isneeded(), True)

        # Wrong file content:
        open(inst.filename, 'w').write('blah blah')
        os.chmod(inst.filename, 0o755)
        self.assertIs(inst.isneeded(), True)

        # Correct content, wrong perms:
        open(inst.filename, 'w').write(actions.WIFI_PM_DISABLE)
        os.chmod(inst.filename, 0o644)
        self.assertIs(inst.isneeded(), True)
        os.chmod(inst.filename, 0o777)
        self.assertIs(inst.isneeded(), True)

        # All good:
        os.chmod(inst.filename, 0o755)
        self.assertIs(inst.isneeded(), False)

    def _check_file(self, inst):
        self.assertEqual(
            open(inst.filename, 'r').read(),
            actions.WIFI_PM_DISABLE
        )
        st = os.stat(inst.filename)
        self.assertEqual(stat.S_IMODE(st.st_mode), 0o755)

    def test_perform(self):
        tmp = TempDir()
        inst = actions.wifi_pm_disable(etcdir=tmp.dir)

        # Missing directories
        with self.assertRaises(FileNotFoundError) as cm:
            inst.perform()
        self.assertEqual(cm.exception.filename, inst.filename)

        # Missing file
        tmp.mkdir('pm')
        tmp.mkdir('pm', 'power.d')
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
        os.chmod(inst.filename, 0o777)
        self.assertIsNone(inst.perform())
        self._check_file(inst)

        # Action didn't need to be performed:
        self.assertIsNone(inst.perform())
        self._check_file(inst)

