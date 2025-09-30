# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: 2005-2016 System76, Inc.

"""
Base classes and helpers for unit tests.
"""

import os
from os import path
import tempfile
import shutil


class TempDir:
    def __init__(self, prefix='unittest.'):
        self.dir = tempfile.mkdtemp(prefix=prefix)

    def __del__(self):
        shutil.rmtree(self.dir)

    def join(self, *parts):
        return path.join(self.dir, *parts)

    def listdir(self, *parts):
        return sorted(os.listdir(self.join(*parts)))

    def mkdir(self, *parts):
        dirname = self.join(*parts)
        os.mkdir(dirname)
        return dirname

    def makedirs(self, *parts):
        dirname = self.join(*parts)
        os.makedirs(dirname)
        return dirname

    def touch(self, *parts):
        filename = self.join(*parts)
        open(filename, 'xb').close()
        return filename

    def write(self, content, *parts):
        filename = self.join(*parts)
        open(filename, 'xb').write(content)
        return filename

    def remove(self, *parts):
        os.remove(self.join(*parts))

