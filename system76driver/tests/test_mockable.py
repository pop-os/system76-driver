# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2005-2016 System76, Inc.

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
