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
Unit tests for `system76driver.gtk` module.
"""

from unittest import TestCase
import distro
from collections import namedtuple

from gi.repository import Gtk

import system76driver
from system76driver.actions import random_id
from system76driver import gtk


DummyArgs = namedtuple('DummyArgs', 'home dry')


class TestUI(TestCase):
    def test_init(self):
        args = DummyArgs('/home/oem', False)
        product = {
            'name': 'Gazelle Professional',
            'drivers': [],
            'prefs': [],
        }
        ui = gtk.UI('gazp9', product, args)
        self.assertIsNone(ui.thread)
        self.assertEqual(ui.model, 'gazp9')
        self.assertIs(ui.product, product)
        self.assertIs(ui.args, args)
        self.assertIsInstance(ui.builder, Gtk.Builder)
        self.assertIsInstance(ui.window, Gtk.Window)
        self.assertEqual(
            ui.builder.get_object('sysName').get_text(),
            'Gazelle Professional'
        )
        self.assertEqual(
            ui.builder.get_object('sysModel').get_text(),
            'gazp9'
        )
        self.assertEqual(
            ui.builder.get_object('ubuntuVersion').get_text(),
            '{} {} ({})'.format(*distro.linux_distribution())
        )
        self.assertEqual(
            ui.builder.get_object('driverVersion').get_text(),
            system76driver.__version__
        )

        model = random_id()
        name = random_id()
        product = {'name': name}
        ui = gtk.UI(model, product, args)
        self.assertIsNone(ui.thread)
        self.assertEqual(ui.model, model)
        self.assertIs(ui.product, product)
        self.assertEqual(ui.product, {'name': name})
        self.assertIs(ui.args, args)
        self.assertIsInstance(ui.builder, Gtk.Builder)
        self.assertIsInstance(ui.window, Gtk.Window)
        self.assertEqual(ui.builder.get_object('sysName').get_text(), name)
        self.assertEqual(ui.builder.get_object('sysModel').get_text(), model)
        self.assertEqual(
            ui.builder.get_object('ubuntuVersion').get_text(),
            '{} {} ({})'.format(*distro.linux_distribution())
        )
        self.assertEqual(
            ui.builder.get_object('driverVersion').get_text(),
            system76driver.__version__
        )

    def test_set_notify(self):
        args = DummyArgs('/home/oem', False)
        ui = gtk.UI('gazp9', {'name': 'Gazelle Professional'}, args)
        text = random_id()
        self.assertIsNone(ui.set_notify('gtk-execute', text))
        self.assertEqual(ui.notify_text.get_text(), text)
