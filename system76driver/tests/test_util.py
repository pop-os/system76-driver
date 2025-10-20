# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2005-2016 System76, Inc.

"""
Unit tests for `system76driver.util` module.
"""

from unittest import TestCase
import os
from os import path
import shutil

from .helpers import TempDir
from system76driver.mockable import SubProcess
from system76driver import util


class TestFunctions(TestCase):
    def test_create_tmp_logs(self):
        SubProcess.reset(mocking=False)
        (tmp, tgz) = util.create_tmp_logs(func=None)
        self.assertTrue(path.isdir(tmp))
        self.assertTrue(tmp.startswith('/tmp/logs.'))
        self.assertEqual(
            sorted(os.listdir(tmp)),
            ['system76-logs', 'system76-logs.tgz'],
        )
        self.assertEqual(tgz, path.join(tmp, 'system76-logs.tgz'))
        self.assertTrue(path.isfile(tgz))
        self.assertTrue(path.isdir(path.join(tmp, 'system76-logs')))
        shutil.rmtree(tmp)

    def test_create_logs(self):
        SubProcess.reset(mocking=False)
        tmp = TempDir()
        tgz = util.create_logs(tmp.dir, func=None)
        self.assertEqual(tgz, tmp.join('system76-logs.tgz'))
        self.assertTrue(path.isfile(tgz))

