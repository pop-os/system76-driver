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

