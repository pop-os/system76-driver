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
