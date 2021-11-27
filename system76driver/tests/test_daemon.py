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
Unit tests for `system76driver.airplane` module.
"""

from unittest import TestCase
import os
import io
import json

from .helpers import TempDir
from system76driver.mockable import SubProcess
from system76driver.actions import random_id
from system76driver import daemon, products


class TestConstants(TestCase):
    def test_NEEDS_AIRPLANE(self):
        self.assertIsInstance(daemon.NEEDS_AIRPLANE, frozenset)
        for key in daemon.NEEDS_AIRPLANE:
            self.assertIsInstance(key, str)
            self.assertIn(key, products.PRODUCTS)

    def test_NEEDS_BRIGHTNESS(self):
        self.assertIsInstance(daemon.NEEDS_BRIGHTNESS, tuple)
        self.assertEqual(len(daemon.NEEDS_BRIGHTNESS),
            len(set(daemon.NEEDS_BRIGHTNESS))
        )
        for key in daemon.NEEDS_BRIGHTNESS:
            self.assertIsInstance(key, str)
            self.assertIn(key, products.PRODUCTS)

    def test_NEEDS_BRIGHTNESS_ACPI(self):
        self.assertIsInstance(daemon.NEEDS_BRIGHTNESS_ACPI, tuple)
        self.assertEqual(len(daemon.NEEDS_BRIGHTNESS_ACPI),
            len(set(daemon.NEEDS_BRIGHTNESS_ACPI))
        )
        for key in daemon.NEEDS_BRIGHTNESS_ACPI:
            self.assertIsInstance(key, str)
            self.assertIn(key, products.PRODUCTS)
            self.assertIn(key, daemon.NEEDS_BRIGHTNESS)


class TestFunctions(TestCase):
    def test_load_json_conf(self):
        tmp = TempDir()
        f = tmp.join('system76-daemon.json')

        # Missing file:
        self.assertEqual(daemon.load_json_conf(f), {})

        # Invalid JSON:
        open(f, 'x').write('invalid json')
        self.assertEqual(daemon.load_json_conf(f), {})

        # JSON does not contain a dict:
        open(f, 'w').write(json.dumps(['hello', 'world']))
        self.assertEqual(daemon.load_json_conf(f), {})

        # dict is empty:
        open(f, 'w').write(json.dumps({}))
        self.assertEqual(daemon.load_json_conf(f), {})

        # dict has stuffs:
        open(f, 'w').write(json.dumps({'foo': 'bar'}))
        self.assertEqual(daemon.load_json_conf(f), {'foo': 'bar'})

        # dict has random_stuffs:
        key = random_id()
        value = random_id()
        open(f, 'w').write(json.dumps({key: value}))
        self.assertEqual(daemon.load_json_conf(f), {key: value})

    def test_save_json_conf(self):
        tmp = TempDir()
        name = random_id() + '.json'
        f = tmp.join(name)

        # No pre-existing file:
        key = random_id()
        value = random_id()
        conf = {'foo': 'bar', key: value}
        self.assertIsNone(daemon.save_json_conf(f, conf))
        self.assertEqual(json.load(open(f, 'r')), {'foo': 'bar', key: value})
        self.assertEqual(os.listdir(tmp.dir), [name])

        # Pre-existing file:
        key = random_id()
        value = random_id()
        conf = {'bar': 'baz', key: value}
        self.assertIsNone(daemon.save_json_conf(f, conf))
        self.assertEqual(json.load(open(f, 'r')), {'bar': 'baz', key: value})
        self.assertEqual(os.listdir(tmp.dir), [name])

        # Empty conf:
        self.assertIsNone(daemon.save_json_conf(f, {}))
        self.assertEqual(json.load(open(f, 'r')), {})
        self.assertEqual(os.listdir(tmp.dir), [name])

    def test_open_ec(self):
        SubProcess.reset(mocking=True)
        tmp = TempDir()
        tmp.mkdir('kernel')
        tmp.mkdir('kernel', 'debug')
        tmp.mkdir('kernel', 'debug', 'ec')
        tmp.mkdir('kernel', 'debug', 'ec', 'ec0')
        data = os.urandom(256)
        name = tmp.write(data, 'kernel', 'debug', 'ec', 'ec0', 'io')
        fp = daemon.open_ec(sysdir=tmp.dir)
        self.assertIsInstance(fp, io.FileIO)
        self.assertEqual(fp.name, name)
        self.assertIs(fp.closed, False)
        self.assertEqual(fp.mode, 'rb+')
        self.assertEqual(SubProcess.calls, [
            ('check_call', ['modprobe', 'ec_sys', 'write_support'], {}),
        ])
        self.assertEqual(fp.tell(), 0)
        self.assertEqual(fp.read(), data)

    def test_read_int(self):
        data = os.urandom(256)
        tmp = TempDir()
        name = tmp.write(data, 'io')
        fp = open(name, 'rb+')
        fileno = fp.fileno()
        for addr in range(256):
            self.assertEqual(daemon.read_int(fileno, addr), data[addr])
            self.assertEqual(fp.tell(), 0)
        self.assertIs(fp.closed, False)
        self.assertEqual(fp.read(), data)

    def test_write_int(self):
        data1 = os.urandom(256)
        data2 = os.urandom(256)
        tmp = TempDir()
        name = tmp.write(data1, 'io')
        fp = open(name, 'rb+')
        fileno = fp.fileno()
        for i in range(256):
            addr = 255 - i
            self.assertIsNone(daemon.write_int(fileno, addr, data2[addr]))
            self.assertEqual(fp.tell(), 0)
        self.assertIs(fp.closed, False)
        self.assertEqual(fp.read(), data2)

    def test_bit6_is_set(self):
        self.assertTrue(daemon.bit6_is_set(0b01000000))
        self.assertTrue(daemon.bit6_is_set(0b11111111))
        self.assertFalse(daemon.bit6_is_set(0b10111111))
        self.assertFalse(daemon.bit6_is_set(0b00000000))

    def test_set_bit6(self):
        self.assertEqual(daemon.set_bit6(0b00000000), 0b01000000)
        self.assertEqual(daemon.set_bit6(0b00000001), 0b01000001)
        self.assertEqual(daemon.set_bit6(0b01000000), 0b01000000)
        self.assertEqual(daemon.set_bit6(0b11111111), 0b11111111)

    def test_clear_bit6(self):
        self.assertEqual(daemon.clear_bit6(0b11111111), 0b10111111)
        self.assertEqual(daemon.clear_bit6(0b01000000), 0b00000000)
        self.assertEqual(daemon.clear_bit6(0b10111111), 0b10111111)
        self.assertEqual(daemon.clear_bit6(0b00000000), 0b00000000)

    def test_read_state(self):
        tmp = TempDir()
        state_file = tmp.write(b'junk\n', 'state')
        with self.assertRaises(ValueError) as cm:
            daemon.read_state(state_file)
        self.assertEqual(str(cm.exception),
             "invalid literal for int() with base 10: b'junk\\n'"
        )
        open(state_file, 'w').write('0\n')
        self.assertIs(daemon.read_state(state_file), False)
        open(state_file, 'w').write('1\n')
        self.assertIs(daemon.read_state(state_file), True)

    def test_write_state(self):
        tmp = TempDir()
        state_file = tmp.write(b'junk\n', 'state')
        self.assertIsNone(daemon.write_state(state_file, False))
        self.assertEqual(open(state_file, 'r').read(), '0\n')
        self.assertIsNone(daemon.write_state(state_file, True))
        self.assertEqual(open(state_file, 'r').read(), '1\n')

    def test_sync_led(self):
        # Test syncing False first:
        data = os.urandom(256)
        tmp = TempDir()
        name = tmp.write(data, 'io')
        fp = open(name, 'rb+')
        fd = fp.fileno()
        self.assertIsNone(daemon.sync_led(fd, False))
        self.assertFalse(daemon.bit6_is_set(daemon.read_int(fd, 0xD9)))
        self.assertIsNone(daemon.sync_led(fd, True))
        self.assertTrue(daemon.bit6_is_set(daemon.read_int(fd, 0xD9)))

        # Test syncing True first:
        data = os.urandom(256)
        tmp = TempDir()
        name = tmp.write(data, 'io')
        fp = open(name, 'rb+')
        fd = fp.fileno()
        self.assertIsNone(daemon.sync_led(fd, True))
        self.assertTrue(daemon.bit6_is_set(daemon.read_int(fd, 0xD9)))
        self.assertIsNone(daemon.sync_led(fd, False))
        self.assertFalse(daemon.bit6_is_set(daemon.read_int(fd, 0xD9)))


class TestBrightness(TestCase):
    def test_init(self):
        inst = daemon.Brightness('gazp9', 'intel_backlight')
        self.assertEqual(inst.model, 'gazp9')
        self.assertEqual(inst.name, 'intel_backlight')
        self.assertEqual(inst.key, 'gazp9.intel_backlight')
        self.assertIsNone(inst.current)
        self.assertEqual(inst.backlight_dir,
            '/sys/class/backlight/intel_backlight'
        )
        self.assertEqual(inst.max_brightness_file,
            '/sys/class/backlight/intel_backlight/max_brightness'
        )
        self.assertEqual(inst.saved_file,
            '/var/lib/system76-driver/brightness.json'
        )

        tmp = TempDir()
        inst = daemon.Brightness('sabc1', 'acpi_video0', rootdir=tmp.dir)
        self.assertEqual(inst.model, 'sabc1')
        self.assertEqual(inst.name, 'acpi_video0')
        self.assertEqual(inst.key, 'sabc1.acpi_video0')
        self.assertIsNone(inst.current)
        self.assertEqual(inst.backlight_dir,
            tmp.join('sys', 'class', 'backlight', 'acpi_video0')
        )
        self.assertEqual(inst.max_brightness_file,
            tmp.join('sys', 'class', 'backlight', 'acpi_video0', 'max_brightness')
        )
        self.assertEqual(inst.brightness_file,
            tmp.join('sys', 'class', 'backlight', 'acpi_video0', 'brightness')
        )
        self.assertEqual(inst.saved_file,
            tmp.join('var', 'lib', 'system76-driver', 'brightness.json')
        )

    def test_read_max_brightness(self):
        tmp = TempDir()
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)

        # Missing dir
        with self.assertRaises(FileNotFoundError) as cm:
            inst.read_max_brightness()
        self.assertEqual(cm.exception.filename, inst.max_brightness_file)

        # Mising file:
        tmp.makedirs('sys', 'class', 'backlight', 'intel_backlight')
        with self.assertRaises(FileNotFoundError) as cm:
            inst.read_max_brightness()
        self.assertEqual(cm.exception.filename, inst.max_brightness_file)

        # Bad file content:
        open(inst.max_brightness_file, 'x').write('foobar\n')
        with self.assertRaises(ValueError) as cm:
            inst.read_max_brightness()
        self.assertEqual(str(cm.exception),
            "invalid literal for int() with base 10: b'foobar\\n'"
        )

        # Good values
        open(inst.max_brightness_file, 'w').write('0\n')
        self.assertEqual(inst.read_max_brightness(), 0)
        open(inst.max_brightness_file, 'w').write('17\n')
        self.assertEqual(inst.read_max_brightness(), 17)
        open(inst.max_brightness_file, 'w').write('1776\n')
        self.assertEqual(inst.read_max_brightness(), 1776)

    def test_read_brightness(self):
        tmp = TempDir()
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)

        # Missing dir
        with self.assertRaises(FileNotFoundError) as cm:
            inst.read_brightness()
        self.assertEqual(cm.exception.filename, inst.brightness_file)

        # Mising file:
        tmp.makedirs('sys', 'class', 'backlight', 'intel_backlight')
        with self.assertRaises(FileNotFoundError) as cm:
            inst.read_brightness()
        self.assertEqual(cm.exception.filename, inst.brightness_file)

        # Bad file content
        open(inst.brightness_file, 'x').write('foobar\n')
        with self.assertRaises(ValueError) as cm:
            inst.read_brightness()
        self.assertEqual(str(cm.exception),
            "invalid literal for int() with base 10: b'foobar\\n'"
        )

        # Good values
        open(inst.brightness_file, 'w').write('0\n')
        self.assertEqual(inst.read_brightness(), 0)
        open(inst.brightness_file, 'w').write('17\n')
        self.assertEqual(inst.read_brightness(), 17)
        open(inst.brightness_file, 'w').write('1776\n')
        self.assertEqual(inst.read_brightness(), 1776)

    def test_write_brightness(self):
        tmp = TempDir()
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)

        # Missing dir
        with self.assertRaises(FileNotFoundError) as cm:
            inst.write_brightness(303)
        self.assertEqual(cm.exception.filename, inst.brightness_file)

        # No file:
        tmp.makedirs('sys', 'class', 'backlight', 'intel_backlight')
        self.assertIsNone(inst.write_brightness(303))
        self.assertEqual(open(inst.brightness_file, 'r').read(), '303')
        self.assertEqual(inst.read_brightness(), 303)

        # Existing file:
        self.assertIsNone(inst.write_brightness(76))
        self.assertEqual(open(inst.brightness_file, 'r').read(), '76')
        self.assertEqual(inst.read_brightness(), 76)

    def test_load(self):
        tmp = TempDir()
        tmp.makedirs('var', 'lib', 'system76-driver')
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)

        # No file:
        self.assertIsNone(inst.load())

        # Bad value in file
        open(inst.saved_file, 'x').write('no json here')
        self.assertIsNone(inst.load())
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': 17.69})
        )
        self.assertIsNone(inst.load())

        # Less than or equal to zero
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': 0})
        )
        self.assertIsNone(inst.load())
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': -1})
        )
        self.assertIsNone(inst.load())

        # One and other good values
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': 1})
        )
        self.assertEqual(inst.load(), 1)
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': 1054})
        )
        self.assertEqual(inst.load(), 1054)

        ############################################################
        # All the same, except this time with a max_brightness file:
        tmp = TempDir()
        tmp.makedirs('var', 'lib', 'system76-driver')
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)
        tmp.makedirs('sys', 'class', 'backlight', 'intel_backlight')
        open(inst.max_brightness_file, 'xb').write(b'5273')

        # No file
        self.assertEqual(inst.load(), 3954)

        # Bad value in file
        open(inst.saved_file, 'x').write('no json here')
        self.assertEqual(inst.load(), 3954)
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': 17.69})
        )
        self.assertEqual(inst.load(), 3954)

        # Less than or equal to zero
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': 0})
        )
        self.assertEqual(inst.load(), 3954)
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': -1})
        )
        self.assertEqual(inst.load(), 3954)

        # One and other good values
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': 1})
        )
        self.assertEqual(inst.load(), 1)
        open(inst.saved_file, 'w').write(
            json.dumps({'gazp9.intel_backlight': 1054})
        )
        self.assertEqual(inst.load(), 1054)

    def test_save(self):
        tmp = TempDir()
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)

        # Missing dir
        with self.assertRaises(FileNotFoundError) as cm:
            inst.save(303)
        self.assertTrue(cm.exception.filename.startswith(inst.saved_file + '.'))

        # No file:
        tmp.makedirs('var', 'lib', 'system76-driver')
        self.assertIsNone(inst.save(303))
        self.assertEqual(json.load(open(inst.saved_file, 'r')),
            {'gazp9.intel_backlight': 303}
        )
        self.assertEqual(inst.load(), 303)

        # Existing file:
        json.dump({'gazp9': 70}, open(inst.saved_file, 'w'))
        self.assertIsNone(inst.save(76))
        self.assertEqual(
            json.load(open(inst.saved_file, 'r')),
            {'gazp9.intel_backlight': 76, 'gazp9': 70}
        )
        self.assertEqual(inst.load(), 76)

        # Existing file with existing 'gazp9' entry:
        self.assertIsNone(inst.save(69))
        self.assertEqual(
            json.load(open(inst.saved_file, 'r')),
            {'gazp9.intel_backlight': 69, 'gazp9': 70}
        )
        self.assertEqual(inst.load(), 69)

    def test_restore(self):
        # Test when all needed files/dirs are missing:
        tmp = TempDir()
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)
        self.assertIsNone(inst.restore())

        # When /var/lib/system76-driver/brightness.json file exists, but the
        # /sys/class/backlight/intel_backlight/ dir doesn't exist, should get a
        # FileNotFoundError:
        tmp = TempDir()
        tmp.makedirs('var', 'lib', 'system76-driver')
        tmp.write(b'{"gazp9.intel_backlight":790}',
                'var', 'lib', 'system76-driver', 'brightness.json')
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)
        with self.assertRaises(FileNotFoundError) as cm:
            inst.restore()
        self.assertEqual(cm.exception.filename,
            tmp.join('sys', 'class', 'backlight', 'intel_backlight', 'brightness')
        )

        # When /var/lib/system76-driver/brightness.json file does *not* exist,
        # should default to 75% of of max_brightness:
        tmp = TempDir()
        tmp.makedirs('sys', 'class', 'backlight', 'intel_backlight')
        tmp.write(b'1054\n',
            'sys', 'class', 'backlight', 'intel_backlight', 'max_brightness')
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)
        self.assertIsNone(inst.restore())
        self.assertEqual(inst.current, 790)
        self.assertEqual(open(inst.brightness_file, 'rb').read(), b'790')

        # Should overright contents of
        # /sys/class/backlight/intel_backlight/brightness file:
        tmp = TempDir()
        tmp.makedirs('sys', 'class', 'backlight', 'intel_backlight')
        tmp.write(b'1054\n',
            'sys', 'class', 'backlight', 'intel_backlight', 'max_brightness')
        tmp.write(b'42\n',
            'sys', 'class', 'backlight', 'intel_backlight', 'brightness')
        inst = daemon.Brightness('gazp9', 'intel_backlight', rootdir=tmp.dir)
        self.assertIsNone(inst.restore())
        self.assertEqual(inst.current, 790)
        self.assertEqual(open(inst.brightness_file, 'rb').read(), b'790')
