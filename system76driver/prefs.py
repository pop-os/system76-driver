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
Actions that modify default preferences.
"""

from gettext import gettext as _

from .mockable import SubProcess
from .actions import Action


def set_two_finger(user):
    cmd = [
        'su', user, '-c',
        'gsettings',
        'set',
        'org.gnome.settings-daemon.peripherals.touchpad',
        'scroll-method',
        'two-finger-scrolling',
    ]
    SubProcess.check_call(cmd)
