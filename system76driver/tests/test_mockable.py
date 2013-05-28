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
Unit tests for `system76driver.mockable` module.
"""

from unittest import TestCase
import subprocess

from system76driver.mockable import SubProcess


class TestSubProcess(TestCase):
    def test_reset(self):
        calls = SubProcess.calls
        outputs = SubProcess.outputs

        SubProcess.calls.extend(['foo', 'bar'])
        SubProcess.outputs.append(b'baz')
        self.assertIsNone(SubProcess.reset())
        self.assertIs(SubProcess.mocking, False)
        self.assertEqual(SubProcess.calls, [])
        self.assertIs(SubProcess.calls, calls)
        self.assertEqual(SubProcess.outputs, [])
        self.assertIs(SubProcess.outputs, outputs)

        SubProcess.calls.extend(['foo', 'bar'])
        SubProcess.outputs.append(b'baz')
        self.assertIsNone(SubProcess.reset(True))
        self.assertIs(SubProcess.mocking, True)
        self.assertEqual(SubProcess.calls, [])
        self.assertIs(SubProcess.calls, calls)
        self.assertEqual(SubProcess.outputs, [])
        self.assertIs(SubProcess.outputs, outputs)

        SubProcess.calls.extend(['foo', 'bar'])
        SubProcess.outputs.append(b'baz')
        self.assertIsNone(SubProcess.reset(True, [b'stuff', b'junk']))
        self.assertIs(SubProcess.mocking, True)
        self.assertEqual(SubProcess.calls, [])
        self.assertIs(SubProcess.calls, calls)
        self.assertEqual(SubProcess.outputs, [b'stuff', b'junk'])
        self.assertIs(SubProcess.outputs, outputs)

    def test_check_call(self):
        SubProcess.reset(mocking=True)
        self.assertIsNone(SubProcess.check_call(['/no/such', 'thing']))
        self.assertEqual(SubProcess.calls, [
            ('check_call', ['/no/such', 'thing'], {}),
        ])
        self.assertEqual(SubProcess.outputs, [])
        self.assertIsNone(SubProcess.check_call(['/nope'], foo='bar'))
        self.assertEqual(SubProcess.calls, [
            ('check_call', ['/no/such', 'thing'], {}),
            ('check_call', ['/nope'], {'foo': 'bar'}),
        ])
        self.assertEqual(SubProcess.outputs, [])

        SubProcess.reset(mocking=False)
        self.assertEqual(SubProcess.check_call(['/bin/true']), 0)
        self.assertEqual(SubProcess.calls, [])
        self.assertEqual(SubProcess.outputs, [])

        with self.assertRaises(subprocess.CalledProcessError) as cm:
            SubProcess.check_call(['/bin/false'])
        self.assertEqual(cm.exception.cmd, ['/bin/false'])
        self.assertEqual(cm.exception.returncode, 1)
        self.assertEqual(SubProcess.calls, [])
        self.assertEqual(SubProcess.outputs, [])

        with self.assertRaises(subprocess.TimeoutExpired) as cm:
            SubProcess.check_call(['/bin/sleep', '2'], timeout=0.5)
        self.assertEqual(cm.exception.cmd, ['/bin/sleep', '2'])
        self.assertEqual(cm.exception.timeout, 0.5)
        self.assertEqual(SubProcess.calls, [])
        self.assertEqual(SubProcess.outputs, [])

    def test_check_output(self):
        SubProcess.reset(mocking=True, outputs=[b'one', b'two'])
        self.assertEqual(SubProcess.check_output(['/no/such', 'thing']), b'one')
        self.assertEqual(SubProcess.calls, [
            ('check_output', ['/no/such', 'thing'], {}),
        ])
        self.assertEqual(SubProcess.outputs, [b'two'])
        self.assertEqual(SubProcess.check_output(['/nope'], foo='bar'), b'two')
        self.assertEqual(SubProcess.calls, [
            ('check_output', ['/no/such', 'thing'], {}),
            ('check_output', ['/nope'], {'foo': 'bar'}),
        ])
        self.assertEqual(SubProcess.outputs, [])

        SubProcess.reset(mocking=False)
        self.assertEqual(
            SubProcess.check_output(['/bin/echo', 'hello world']),
            b'hello world\n'
        )
        self.assertEqual(SubProcess.calls, [])
        self.assertEqual(SubProcess.outputs, [])

        with self.assertRaises(subprocess.CalledProcessError) as cm:
            SubProcess.check_output(['/bin/false'])
        self.assertEqual(cm.exception.cmd, ['/bin/false'])
        self.assertEqual(cm.exception.returncode, 1)
        self.assertEqual(SubProcess.calls, [])
        self.assertEqual(SubProcess.outputs, [])

        with self.assertRaises(subprocess.TimeoutExpired) as cm:
            SubProcess.check_output(['/bin/sleep', '2'], timeout=0.5)
        self.assertEqual(cm.exception.cmd, ['/bin/sleep', '2'])
        self.assertEqual(cm.exception.timeout, 0.5)
        self.assertEqual(SubProcess.calls, [])
        self.assertEqual(SubProcess.outputs, [])
