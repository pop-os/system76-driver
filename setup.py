#!/usr/bin/python3

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
Install `system76driver`.
"""

import sys
if sys.version_info < (3, 4):
    sys.exit('ERROR: `system76driver` requires Python 3.4 or newer')

import os
from os import path
import subprocess
from distutils.core import setup
from distutils.cmd import Command

import system76driver
from system76driver.tests.run import run_tests


SCRIPTS = [
    'system76-driver',
    'system76-driver-cli',
]


def run_pyflakes3():
    pyflakes3 = '/usr/bin/pyflakes3'
    if not os.access(pyflakes3, os.R_OK | os.X_OK):
        print('WARNING: cannot read and execute: {!r}'.format(pyflakes3))
        return
    tree = path.dirname(path.abspath(__file__))
    names = [
        'system76driver',
        'setup.py',
        'system76-daemon',
    ] + SCRIPTS
    cmd = [pyflakes3] + [path.join(tree, name) for name in names]
    print('check_call:', cmd)
    subprocess.check_call(cmd)
    print('[pyflakes3 checks passed]')


class Test(Command):
    description = 'run unit tests and doc tests'

    user_options = [
        ('skip-gtk', None, 'Skip GTK related tests'),
    ]

    def initialize_options(self):
        self.skip_gtk = 0

    def finalize_options(self):
        pass

    def run(self):
        if not run_tests(self.skip_gtk):
            raise SystemExit(2)
        run_pyflakes3()


setup(
    name='system76driver',
    version=system76driver.__version__,
    description='hardware-specific enhancements for System76 products',
    url='https://copr.fedorainfracloud.org/coprs/szydell/system76/',
    author='System76, Inc.',
    author_email='dev@system76.com',
    maintainer='Marcin Szydelski',
    maintainer_email='marcin@szydelscy.pl',
    license='GPLv2+',
    cmdclass={'test': Test},
    packages=[
        'system76driver',
        'system76driver.tests'
    ],
    scripts=SCRIPTS,
    package_data={
        'system76driver': ['data/*'],
    },
    data_files=[
        ('share/applications', ['system76-driver.desktop']),
        ('share/icons/hicolor/scalable/apps', ['system76-driver.svg']),
    ],
)
