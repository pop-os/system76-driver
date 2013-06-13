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
Unit tests for `system76driver.airplane` module.
"""

from unittest import TestCase
import os
import io

from .helpers import TempDir
from system76driver.mockable import SubProcess
from system76driver import airplane


class TestFunctions(TestCase):
    def test_open_etc(self):
        SubProcess.reset(mocking=True)
        tmp = TempDir()
        tmp.mkdir('kernel')
        tmp.mkdir('kernel', 'debug')
        tmp.mkdir('kernel', 'debug', 'ec')
        tmp.mkdir('kernel', 'debug', 'ec', 'ec0')
        data = os.urandom(256)
        name = tmp.write(data, 'kernel', 'debug', 'ec', 'ec0', 'io')
        fp = airplane.open_ec(sysdir=tmp.dir)
        self.assertIsInstance(fp, io.BufferedRandom)
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
            self.assertEqual(airplane.read_int(fileno, addr), data[addr])
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
            self.assertIsNone(airplane.write_int(fileno, addr, data2[addr]))
            self.assertEqual(fp.tell(), 0)
        self.assertIs(fp.closed, False)
        self.assertEqual(fp.read(), data2)

    def test_bit6_is_set(self):
        self.assertTrue( airplane.bit6_is_set(0b01000000))
        self.assertTrue( airplane.bit6_is_set(0b11111111))
        self.assertFalse(airplane.bit6_is_set(0b10111111))
        self.assertFalse(airplane.bit6_is_set(0b00000000))

    def test_set_bit6(self):
        self.assertEqual(airplane.set_bit6(0b00000000), 0b01000000)
        self.assertEqual(airplane.set_bit6(0b00000001), 0b01000001)
        self.assertEqual(airplane.set_bit6(0b01000000), 0b01000000)
        self.assertEqual(airplane.set_bit6(0b11111111), 0b11111111)

    def test_clear_bit6(self):
        self.assertEqual(airplane.clear_bit6(0b11111111), 0b10111111)
        self.assertEqual(airplane.clear_bit6(0b01000000), 0b00000000)
        self.assertEqual(airplane.clear_bit6(0b10111111), 0b10111111)
        self.assertEqual(airplane.clear_bit6(0b00000000), 0b00000000)

    def test_toggle_bit6(self):
        self.assertEqual(airplane.toggle_bit6(0b00000000), 0b01000000)
        self.assertEqual(airplane.toggle_bit6(0b00000001), 0b01000001)
        self.assertEqual(airplane.toggle_bit6(0b11111111), 0b10111111)
        self.assertEqual(airplane.toggle_bit6(0b01000000), 0b00000000)

    def test_read_state(self):
        tmp = TempDir()
        state_file = tmp.write(b'junk\n', 'state')
        with self.assertRaises(KeyError) as cm:
            airplane.read_state(state_file)
        self.assertEqual(str(cm.exception), repr('junk\n'))
        open(state_file, 'w').write('0\n')
        self.assertIs(airplane.read_state(state_file), False)
        open(state_file, 'w').write('1\n')
        self.assertIs(airplane.read_state(state_file), True)

    def test_write_state(self):
        tmp = TempDir()
        state_file = tmp.write(b'junk\n', 'state')
        self.assertIsNone(airplane.write_state(state_file, False))
        self.assertEqual(open(state_file, 'r').read(), '0\n')
        self.assertIsNone(airplane.write_state(state_file, True))
        self.assertEqual(open(state_file, 'r').read(), '1\n')

    def test_sync_led(self):
        # Test syncing False first:
        data = os.urandom(256)
        tmp = TempDir()
        name = tmp.write(data, 'io')
        fp = open(name, 'rb+')
        fd = fp.fileno()
        self.assertIsNone(airplane.sync_led(fd, False))
        self.assertFalse(airplane.bit6_is_set(airplane.read_int(fd, 0xD9)))
        self.assertIsNone(airplane.sync_led(fd, True))
        self.assertTrue(airplane.bit6_is_set(airplane.read_int(fd, 0xD9)))

        # Test syncing True first:
        data = os.urandom(256)
        tmp = TempDir()
        name = tmp.write(data, 'io')
        fp = open(name, 'rb+')
        fd = fp.fileno()
        self.assertIsNone(airplane.sync_led(fd, True))
        self.assertTrue(airplane.bit6_is_set(airplane.read_int(fd, 0xD9)))
        self.assertIsNone(airplane.sync_led(fd, False))
        self.assertFalse(airplane.bit6_is_set(airplane.read_int(fd, 0xD9)))
