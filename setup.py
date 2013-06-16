#!/usr/bin/python3

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
Install `system76driver`.
"""

import sys
if sys.version_info < (3, 3):
    sys.exit('ERROR: `system76driver` requires Python 3.3 or newer')

import os
from os import path
from distutils.core import setup
from distutils.cmd import Command

import system76driver
from system76driver.tests.run import run_tests


class Test(Command):
    description = 'run unit tests and doc tests'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if not run_tests():
            raise SystemExit(2)


setup(
    name='system76driver',
    version=system76driver.__version__,
    description='hardware-specific enhancements for System76 products',
    url='https://launchpad.net/system76-driver',
    author='System76, Inc.',
    author_email='dev@system76.com',
    license='GPLv2+',
    packages=[
        'system76driver',
        'system76driver.tests'
    ],
    scripts=[
        'system76-driver',
        'system76-driver-gtk',
    ],
    package_data={
        'system76driver': ['data/*'],
    },
    cmdclass={'test': Test},
)
