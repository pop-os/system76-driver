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
Collect logs and other info for support.
"""

import os
from os import path
import shutil
import tempfile
import distro
import subprocess

from .model import determine_model


def dump_command(base, name, args):
    fp = open(path.join(base, name), 'xt')
    output = subprocess.run(" ".join(args), capture_output=True, shell=True, text=True)
    fp.write(output.stdout + "\n" + output.stderr)


def dump_path(base, name, src):
    if path.exists(src):
        dst = path.join(base, name)
        dst_dir = path.dirname(dst)
        if not path.isdir(dst_dir):
            os.makedirs(dst_dir)
        assert not path.exists(dst)
        if path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)


def dump_logs(base):
    fp = open(path.join(base, 'systeminfo.txt'), 'x')
    fp.write('System76 Model: {}\n'.format(determine_model()))
    fp.write('OS Version: {}\n'.format(distro.name(pretty=True)))
    fp.write('Kernel Version: {}\n'.format(distro.os.uname().release))

    dump_command(base, "dmesg", ["dmesg"])
    dump_command(base, "dmidecode", ["dmidecode"])
    dump_command(base, "lspci", ["lspci", "-vv"])
    dump_command(base, "lsusb", ["lsusb", "-vv"])
    dump_command(base, "lsblk", ["lsblk", "-f"])
    dump_command(base, "df", ["df", "-h"])
    dump_command(base, "journalctl", ["journalctl", "--since", "yesterday"])
    dump_command(base, "sensors", ["sensors"])
    dump_command(base, "uptime", ["uptime"])
    dump_path(base, "fstab", "/etc/fstab")
    dump_path(base, "apt/sources.list", "/etc/apt/sources.list")
    dump_path(base, "apt/sources.list.d", "/etc/apt/sources.list.d")
    dump_path(base, "syslog", "/var/log/syslog")
    dump_path(base, "Xorg.log", "/var/log/Xorg.0.log")
    dump_path(base, "apt/history", "/var/log/apt/history.log")
    dump_path(base, "apt/history-rotated", "/var/log/apt/history.log.1.gz")
    dump_path(base, "apt/term", "/var/log/apt/term.log")
    dump_path(base, "apt/term-rotated", "/var/log/apt/term.log.1.gz")


def create_tmp_logs(func=dump_logs):
    tmp = tempfile.mkdtemp(prefix='logs.')
    base = path.join(tmp, 'system76-logs')
    os.mkdir(base)
    if func is not None:
        func(base)
    tgz = path.join(tmp, 'system76-logs.tgz')
    cmd = [
        'tar', '-czv',
        '-f', tgz,
        '-C', tmp,
        'system76-logs',
    ]
    subprocess.run(cmd)
    return (tmp, tgz)


def create_logs(homedir, func=dump_logs):
    (tmp, src) = create_tmp_logs(func)
    assert path.isdir(homedir)
    dst = path.join(homedir, path.basename(src))
    shutil.copy(src, dst)
    shutil.rmtree(tmp)
    return dst
