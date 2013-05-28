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

