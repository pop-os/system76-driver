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
Bump version of system76-driver to start work on next release.
"""

import sys
import os
from os import path
import re
import time
from subprocess import check_call, check_output, call

from system76driver import __version__
from system76driver.tests.helpers import TempDir


DISTROS = ('trusty', 'xenial', 'yakkety', 'zesty', 'artful', 'bionic', 'cosmic', 'disco', 'eoan', 'focal')
ALPHA = '~~alpha'

TREE = path.dirname(path.abspath(__file__))
assert TREE == sys.path[0]
assert os.getcwd() == TREE

CHANGELOG = path.join(TREE, 'debian', 'changelog')
INIT = path.join(TREE, 'system76driver', '__init__.py')
SETUP = path.join(TREE, 'setup.py')

assert path.isfile(CHANGELOG)
assert path.isfile(INIT)
assert path.isfile(SETUP)


def confirm():
    while True:
        response = input('  Okay? yes/NO: ').lower()
        if response == 'yes':
            return True
        if response == 'no':
            return False
        print("Please enter 'yes' or 'no'")


def check_for_uncommitted_changes():
    if check_output(['git', 'diff']).decode() != '':
        sys.exit('ERROR: unstaged changes!')
    if check_output(['git', 'diff', '--cached']).decode() != '':
        sys.exit('ERROR: uncommited changes!')


def parse_version_line(line):
    if ALPHA in line:
        raise ValueError('{!r} in current version:\n{!r}'.format(ALPHA, line))
    m = re.match(
        '^system76-driver \(([\.0-9]+)\) ([a-z]+); urgency=(low|medium|high|emergency|critical)$', line
    )
    if m is None:
        raise ValueError('bad version line[0]:\n{!r}'.format(line))
    ver = m.group(1)
    if ver != __version__:
        raise ValueError(
            'changelog != __version: {!r} != {!r}'.format(ver, __version__)
        )
    distro = m.group(2)
    if distro not in DISTROS:
        raise ValueError('bad distro {!r} not in {!r}'.format(distro, DISTROS))
    return (ver, distro)


def bump_version(current):
    (year, month, rev) = current.split('.')
    assert str(int(year)) == year and int(year) >= 14
    assert month in ('04', '10')
    assert str(int(rev)) == rev and int(rev) >= 0
    return '{}.{}.{}'.format(year, month, int(rev) + 1)


def build_author_line():
    user = check_output(['git', 'config', '--get', 'user.name']).decode().strip()
    email = check_output(['git', 'config', '--get', 'user.email']).decode().strip()
    author = ' '.join((user, '<' + email + '>'))
    ts = time.strftime('%a, %d %b %Y %H:%M:%S %z', time.localtime())
    return ' -- {}  {}\n'.format(author, ts)


def iter_new_changelog_lines(new, newdeb, distro):
    yield 'system76-driver ({}) {}; urgency=low\n'.format(newdeb, distro)
    yield '\n'
    yield '  * Daily WIP for {}\n'.format(new)
    yield '\n'
    yield build_author_line()
    yield '\n'


def iter_new_init_lines(new, init_lines):
    found_version = False
    for line in init_lines:
        if line.startswith('__version__'):
            assert found_version is False
            found_version = True
            yield '__version__ = {!r}\n'.format(new)
        else:
            yield line


# Make sure there are no uncommited changes in the tree:
check_for_uncommitted_changes()

# Read existing changelog and __init__.py lines:
with open(CHANGELOG, 'r') as fp:
    changelog_lines = fp.readlines()
with open(INIT, 'r') as fp:
    init_lines = fp.readlines()

# Parse out current version and distro, bump version:
(current, distro) = parse_version_line(changelog_lines[0])
assert current == __version__
new = bump_version(current)
assert new != __version__
newdeb = new + ALPHA

# Build new changelog and __init__.py lines:
new_changelog_lines = list(iter_new_changelog_lines(new, newdeb, distro))
new_init_lines = list(iter_new_init_lines(new, init_lines))
assert len(new_changelog_lines) == 6
assert len(new_init_lines) == len(init_lines)

# Again, make sure there are no uncommited changes in the tree:
check_for_uncommitted_changes()

# Write new changelog and __init__.py lines:
with open(CHANGELOG, 'w') as fp:
    fp.writelines(new_changelog_lines + changelog_lines)
with open(INIT, 'w') as fp:
    fp.writelines(new_init_lines)

# Confirm before we make the commit:
print('-' * 80)
call(['git', 'diff'])
print('-' * 80)
print('Source tree is {!r}'.format(TREE))
print(
    'Will bump {!r} version from {!r} to {!r}'.format(distro, current, newdeb)
)
if not confirm():
    print('')
    print('Version bump not committed, reverting changes...')
    check_call(['git', 'checkout', '--', CHANGELOG, INIT])
    print('Goodbye.')
    sys.exit(0)

# Make the commit:
check_call(['git', 'commit', CHANGELOG, INIT, '-m', 'Bump version to {}'.format(newdeb)])
check_call(['git', 'push'])
print('-' * 80)
print('{!r} is now at version {!r}'.format(distro, newdeb))
