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
Unit tests for `system76driver.model` module.
"""

from unittest import TestCase

from system76driver.mockable import SubProcess
from system76driver import model


OUTPUTS = (
    b'CCF59000-5FBA-0000-0000-000000000000\n',
    b'Gazelle Professional\n',
    b'Gazelle Professional\n',
    b'gazp7\n',
)

EXPECTED = (
    ('system-uuid', 'CCF59000-5FBA-0000-0000-000000000000'),
    ('baseboard-product-name', 'Gazelle Professional'),
    ('system-product-name', 'Gazelle Professional'),
    ('system-version', 'gazp7'),
)


class TestConstants(TestCase):
    def test_KEYWORDS(self):
        self.assertIsInstance(model.KEYWORDS, tuple)
        self.assertEqual(len(model.KEYWORDS), 4)
        for keyword in model.KEYWORDS:
            self.assertIsInstance(keyword, str)

    def test_TABLES(self):
        self.assertIsInstance(model.TABLES, dict)
        self.assertEqual(len(model.TABLES), 4)
        self.assertEqual(set(model.TABLES), set(model.KEYWORDS))
        for (key, value) in model.TABLES.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)
            self.assertGreater(len(value), 0)
            for (k, v) in value.items():
                self.assertIsInstance(k, str)
                self.assertIsInstance(v, str)
        # 'system-version' is currently always the same:
        for (k, v) in model.TABLES['system-version'].items():
            self.assertEqual(k, v)


class TestFunctions(TestCase):
    def test_dmidecode(self):
        SubProcess.reset(True, [b'bar\n'])
        self.assertEqual(model.dmidecode('foo'), 'bar')
        self.assertEqual(SubProcess.calls, [
            ('check_output', ['sudo', 'dmidecode', '-s', 'foo'], {}),
        ])
        self.assertEqual(SubProcess.outputs, [])

    def test_get_dmi_info(self):
        SubProcess.reset(True, OUTPUTS)
        self.assertEqual(model.get_dmi_info(), dict(EXPECTED))
        self.assertEqual(SubProcess.calls, [
            ('check_output', ['sudo', 'dmidecode', '-s', 'system-uuid'], {}),
            ('check_output', ['sudo', 'dmidecode', '-s', 'baseboard-product-name'], {}),
            ('check_output', ['sudo', 'dmidecode', '-s', 'system-product-name'], {}),
            ('check_output', ['sudo', 'dmidecode', '-s', 'system-version'], {}),
        ])
        self.assertEqual(SubProcess.outputs, [])

    def test_determine_model_1(self):
        """
        Test `determine_model()` when *info* is provided.
        """
        SubProcess.reset(True, OUTPUTS)
        self.assertEqual(model.determine_model(), 'gazp7')
        self.assertEqual(SubProcess.calls, [
            ('check_output', ['sudo', 'dmidecode', '-s', 'system-uuid'], {}),
            ('check_output', ['sudo', 'dmidecode', '-s', 'baseboard-product-name'], {}),
            ('check_output', ['sudo', 'dmidecode', '-s', 'system-product-name'], {}),
            ('check_output', ['sudo', 'dmidecode', '-s', 'system-version'], {}),
        ])
        self.assertEqual(SubProcess.outputs, [])

    def test_determine_model_2(self):
        """
        Test `determine_model()` when *info* is provided.
        """
        SubProcess.reset(True)

        # system-uuid:
        info = {'system-uuid': '00000000-0000-0000-0000-000000000001'}
        self.assertEqual(model.determine_model(info), 'koap1')

        # baseboard-product-name:
        info = {'system-uuid': 'nope', 'baseboard-product-name': 'Z35FM'}
        self.assertEqual(model.determine_model(info), 'daru1')

        info = {'system-uuid': 'nope', 'baseboard-product-name': 'Z35F'}
        self.assertEqual(model.determine_model(info), 'daru1')

        info = {'system-uuid': 'nope', 'baseboard-product-name': 'MS-1221'}
        self.assertEqual(model.determine_model(info), 'daru2')

        info = {'system-uuid': 'nope', 'baseboard-product-name': 'MS-1221'}
        self.assertEqual(model.determine_model(info), 'daru2')

        # system-uuid:
        for (key, value) in model.TABLES['system-uuid'].items():
            info = {'system-uuid': key}
            self.assertEqual(model.determine_model(info), value)

        # baseboard-product-name:
        for (key, value) in model.TABLES['baseboard-product-name'].items():
            info = {
                'system-uuid': 'nope',
                'baseboard-product-name': key,
            }
            self.assertEqual(model.determine_model(info), value)

        # system-product-name:
        for (key, value) in model.TABLES['system-product-name'].items():
            info = {
                'system-uuid': 'nope',
                'baseboard-product-name': 'nope',
                'system-product-name': key,
            }
            self.assertEqual(model.determine_model(info), value)

        # system-version:
        for (key, value) in model.TABLES['system-version'].items():
            info = {
                'system-uuid': 'nope',
                'baseboard-product-name': 'nope',
                'system-product-name': 'nope',
                'system-version': key,
            }
            self.assertEqual(model.determine_model(info), value)

        # non-System76:
        info = {
            'system-uuid': 'nope',
            'baseboard-product-name': 'nope',
            'system-product-name': 'nope',
            'system-version': 'nope',
        }
        self.assertEqual(model.determine_model(info), 'nonsystem76')

        # No calls should have resulted:
        self.assertEqual(SubProcess.calls, [])
        self.assertEqual(SubProcess.outputs, [])

