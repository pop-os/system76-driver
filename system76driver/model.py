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
Determin model of System76 product.
"""

from .mockable import SubProcess


KEYWORDS = (
    'system-uuid',
    'baseboard-product-name',
    'system-product-name',
    'system-version',
)

SYSTEM_UUID = {
    '00000000-0000-0000-0000-000000000001': 'koap1',
}


def dmidecode(keyword):
    cmd = ['sudo', 'dmidecode', '-s', keyword]
    return SubProcess.check_output(cmd).decode('utf-8').strip()


def get_dmi_info():
    return dict(
        (keyword, dmidecode(keyword)) for keyword in KEYWORDS
    )


def determine_model(info=None):
    """
    Determine the System76 model number.
    """
    if info is None:
        info = get_dmi_info()
    
    # Determine system unique value    
    b = os.popen('sudo dmidecode -s system-uuid')
