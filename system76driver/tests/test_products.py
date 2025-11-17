# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2005-2016 System76, Inc.

"""
Unit tests for `system76driver.products` module.
"""

from unittest import TestCase

from system76driver.mockable import SubProcess
from system76driver import actions, products


OUTPUTS = (
    b'CCF59000-5FBA-0000-0000-000000000000\n',
    b'Gazelle Professional\n',
    b'Gazelle Professional\n',
    b'gazp7\n',
)


class TestConstants(TestCase):
    def test_PRODUCTS(self):
        self.assertIsInstance(products.PRODUCTS, dict)
        for (key, value) in products.PRODUCTS.items():
            SubProcess.reset(True, OUTPUTS)

            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)
            self.assertIn('name', value)
            self.assertIsInstance(value['name'], str)
            self.assertTrue(value['name'])

            self.assertIsInstance(value['drivers'], list)
            for action in value['drivers']:
                self.assertTrue(issubclass(action, actions.Action))
                inst = action()
                text = inst.describe()
                self.assertIsInstance(text, str)
                self.assertTrue(text, text)

            if 'screens' in value:
                screens = value['screens']
                self.assertIsInstance(screens, dict)
                for (edid_md5, description) in screens.items():
                    self.assertIsInstance(edid_md5, str)
                    self.assertIsInstance(description, str)
