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
Mockable subprocess calls.
"""

import subprocess


class SubProcess:
    mocking = False
    calls = []
    outputs = []

    @classmethod
    def reset(cls, mocking=False, outputs=None):
        assert isinstance(mocking, bool)
        cls.mocking = mocking
        cls.calls.clear()
        cls.outputs.clear()
        if outputs:
            assert mocking is True
            for value in outputs:
                assert isinstance(value, bytes)
                cls.outputs.append(value)

    @classmethod
    def check_call(cls, cmd, **kw):
        assert isinstance(cmd, list)
        if cls.mocking:
            cls.calls.append(('check_call', cmd, kw))
        else:
            return subprocess.check_call(cmd, **kw)

    @classmethod
    def check_output(cls, cmd, **kw):
        assert isinstance(cmd, list)
        if cls.mocking:
            cls.calls.append(('check_output', cmd, kw))
            return cls.outputs.pop(0)
        else:
            return subprocess.check_output(cmd, **kw)
