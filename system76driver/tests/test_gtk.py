# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2005-2016 System76, Inc.

"""
Unit tests for `system76driver.gtk` module.
"""

import unittest

import distro
from collections import namedtuple

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import system76driver
from system76driver.actions import random_id
from system76driver import gtk


DummyArgs = namedtuple('DummyArgs', 'home dry')


@unittest.skip("TODO")
class TestUI(unittest.TestCase):
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
