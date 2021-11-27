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
Unit test for the `system76driver` package.
"""

from unittest import TestCase
import os
from os import path
from subprocess import check_call

from .helpers import TempDir
from system76driver.products import PRODUCTS
import system76driver


TREE = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
IN_TREE = path.isfile(path.join(TREE, 'setup.py'))


class TestConstants(TestCase):
    def test_version(self):
        self.assertIsInstance(system76driver.__version__, str)
        (year, month, rev) = system76driver.__version__.split('.')
        self.assertEqual(year, str(int(year)))
        self.assertGreaterEqual(int(year), 13)
        self.assertIn(month, ['04', '10'])
        self.assertEqual(rev, str(int(rev)))
        self.assertGreaterEqual(int(rev), 0)

    def test_VALID_SYS_VENDOR(self):
        self.assertIsInstance(system76driver.VALID_SYS_VENDOR, tuple)
        self.assertIn('System76, Inc.', system76driver.VALID_SYS_VENDOR)
        for value in system76driver.VALID_SYS_VENDOR:
            self.assertIsInstance(value, str)


class TestScripts(TestCase):
    def setUp(self):
        if not IN_TREE:
            self.skipTest('not running tests in-tree')

    def check_script(self, name):
        script = path.join(TREE, name)
        self.assertTrue(path.isfile(script))
        # All the scripts need to be run as root, but you should always be able
        # to do a -h as a normal user:
        check_call([script, '-h'])

    def test_system76_driver(self):
        """
        Test the `system76-driver` Gtk UI script.
        """
        self.check_script('system76-driver')

    def test_system76_driver_cli(self):
        """
        Test the `system76-driver-cli` CLI script.
        """
        self.check_script('system76-driver-cli')

    def test_system76_daemon(self):
        """
        Test the `system76-daemon` CLI script.
        """
        self.check_script('system76-daemon')


class TestDataFiles(TestCase):
    def iter_data_files(self, callback):
        for name in sorted(os.listdir(system76driver.datadir)):
            fullname = path.join(system76driver.datadir, name)
            self.assertTrue(path.isfile(fullname))
            if callback(name):
                yield (name, fullname)

    def test_icc(self):
        for (name, fullname) in self.iter_data_files(lambda n: n.endswith('.icc')):
            self.assertTrue(name.endswith('.icc'))
            (prefix, model, *rest) = name.split('-')
            self.assertEqual(prefix, 'system76')
            self.assertIn(model, PRODUCTS)


class TestFunctions(TestCase):
    def test_read_dmi_id(self):
        tmp = TempDir()
        KEYS = ('sys_vendor', 'product_version')
        VALS = ('System76, Inc.', 'kudp1')

        # Bad dmi/id key:
        bad_keys = tuple(k.upper() for k in KEYS) + ('product_serial', 'product_name')
        for bad in bad_keys:
            with self.assertRaises(ValueError) as cm:
                system76driver.read_dmi_id(bad, sysdir=tmp.dir)
            self.assertEqual(str(cm.exception),
                'bad dmi/id key: {!r}'.format(bad)
            )

        # class/dmi/id dir missing:
        for key in KEYS:
            self.assertIsNone(
                system76driver.read_dmi_id(key, sysdir=tmp.dir)
            )
            self.assertEqual(tmp.listdir(), [])

        # sys_vendor, product_version files misssing:
        tmp.makedirs('class', 'dmi', 'id')
        for key in KEYS:
            self.assertIsNone(
                system76driver.read_dmi_id(key, sysdir=tmp.dir)
            )
            self.assertEqual(tmp.listdir(), ['class'])
            self.assertEqual(tmp.listdir('class'), ['dmi'])
            self.assertEqual(tmp.listdir('class', 'dmi'), ['id'])
            self.assertEqual(tmp.listdir('class', 'dmi', 'id'), [])

        # sys_vendor, product_version files exist:
        for (key, val) in zip(KEYS, VALS):
            tmp.write(val.encode() + b'\n', 'class', 'dmi', 'id', key)
            self.assertEqual(
                system76driver.read_dmi_id(key, sysdir=tmp.dir),
                val
            )
        self.assertEqual(tmp.listdir(), ['class'])
        self.assertEqual(tmp.listdir('class'), ['dmi'])
        self.assertEqual(tmp.listdir('class', 'dmi'), ['id'])
        self.assertEqual(tmp.listdir('class', 'dmi', 'id'), sorted(KEYS))

        # sys_vendor, product_version do not contain valid UTF-8:
        tmp = TempDir()
        tmp.makedirs('class', 'dmi', 'id')
        for (key, val) in zip(KEYS, VALS):
            badval = b'\xff' + val.encode() + b'\n'
            with self.assertRaises(UnicodeDecodeError):
                badval.decode()
            tmp.write(badval, 'class', 'dmi', 'id', key)
            self.assertIsNone(system76driver.read_dmi_id(key, sysdir=tmp.dir))
        self.assertEqual(tmp.listdir(), ['class'])
        self.assertEqual(tmp.listdir('class'), ['dmi'])
        self.assertEqual(tmp.listdir('class', 'dmi'), ['id'])
        self.assertEqual(tmp.listdir('class', 'dmi', 'id'), sorted(KEYS))

        # Non-mocked test, as this can still pass in the build environment:
        for key in KEYS:
            val = system76driver.read_dmi_id(key)
            self.assertIsInstance(val, (type(None), str))
            if isinstance(val, str):
                self.assertEqual(val.strip(), val)

    def test_get_sys_vendor(self):
        get_sys_vendor = system76driver.get_sys_vendor
        tmp = TempDir()

        # class/dmi/id/ dir missing:
        self.assertIsNone(get_sys_vendor(sysdir=tmp.dir))
        self.assertEqual(tmp.listdir(), [])

        # sys_vendor file misssing:
        tmp.makedirs('class', 'dmi', 'id')
        self.assertIsNone(get_sys_vendor(sysdir=tmp.dir))
        self.assertEqual(tmp.listdir(), ['class'])
        self.assertEqual(tmp.listdir('class'), ['dmi'])
        self.assertEqual(tmp.listdir('class', 'dmi'), ['id'])
        self.assertEqual(tmp.listdir('class', 'dmi', 'id'), [])

        # sys_vendor file exists, contains good value:
        for value in system76driver.VALID_SYS_VENDOR:
            tmp = TempDir()
            tmp.makedirs('class', 'dmi', 'id')
            value_b = value.encode() + b'\n'
            tmp.write(value_b, 'class', 'dmi', 'id', 'sys_vendor')
            self.assertEqual(get_sys_vendor(sysdir=tmp.dir), value)
            self.assertEqual(tmp.listdir(), ['class'])
            self.assertEqual(tmp.listdir('class'), ['dmi'])
            self.assertEqual(tmp.listdir('class', 'dmi'), ['id'])
            self.assertEqual(tmp.listdir('class', 'dmi', 'id'), ['sys_vendor'])

        # sys_vendor file exists, contains bad value:
        for value in system76driver.VALID_SYS_VENDOR:
            tmp = TempDir()
            tmp.makedirs('class', 'dmi', 'id')
            bad_value_b = value.upper().encode() + b'\n'
            tmp.write(bad_value_b, 'class', 'dmi', 'id', 'sys_vendor')
            self.assertIsNone(get_sys_vendor(sysdir=tmp.dir))
            self.assertEqual(tmp.listdir(), ['class'])
            self.assertEqual(tmp.listdir('class'), ['dmi'])
            self.assertEqual(tmp.listdir('class', 'dmi'), ['id'])
            self.assertEqual(tmp.listdir('class', 'dmi', 'id'), ['sys_vendor'])

        # Non-mocked test, as this can still pass in the build environment:
        value = get_sys_vendor()
        self.assertIsInstance(value, (type(None), str))
        if isinstance(value, str):
            self.assertEqual(value.strip(), value)

    def test_get_product_version(self):
        get_product_version = system76driver.get_product_version
        tmp = TempDir()
        DPARTS = ('class', 'dmi', 'id')
        SYS_PARTS = DPARTS + ('sys_vendor',)
        VER_PARTS = DPARTS + ('product_version',)

        # class/dmi/id/ dir missing:
        self.assertIsNone(get_product_version(sysdir=tmp.dir))
        self.assertEqual(tmp.listdir(), [])

        # sys_vendor and product_version files misssing:
        tmp.makedirs(*DPARTS)
        self.assertIsNone(get_product_version(sysdir=tmp.dir))
        self.assertEqual(tmp.listdir(), ['class'])
        self.assertEqual(tmp.listdir('class'), ['dmi'])
        self.assertEqual(tmp.listdir('class', 'dmi'), ['id'])
        self.assertEqual(tmp.listdir('class', 'dmi', 'id'), [])

        # product_version file exists, but sys_vendor is missing:
        tmp.write(b'kudu2\n', *VER_PARTS)
        self.assertIsNone(get_product_version(sysdir=tmp.dir))

        # sys_vendor exists but contains a bad value:
        tmp.write(b'Nope\n', *SYS_PARTS)
        self.assertIsNone(get_product_version(sysdir=tmp.dir))

        # sys_vendor file exists and contains a good value:
        for value in system76driver.VALID_SYS_VENDOR:
            tmp.remove(*SYS_PARTS)
            value_b = value.encode() + b'\n'
            tmp.write(value_b, *SYS_PARTS)
            self.assertEqual(get_product_version(sysdir=tmp.dir), 'kudu2')

        # Non-mocked test, as this can still pass in the build environment:
        value = get_product_version()
        self.assertIsInstance(value, (type(None), str))
        if isinstance(value, str):
            self.assertEqual(value.strip(), value)
