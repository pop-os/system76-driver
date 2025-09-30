# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2005-2016 System76, Inc.

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

