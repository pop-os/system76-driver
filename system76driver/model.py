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
Determine model of System76 product.
"""

from . import read_dmi_id
from .mockable import SubProcess


KEYWORDS = (
    'system-uuid',
    'baseboard-product-name',
    'system-product-name',
    'system-version',
)

ALL_KEYWORDS = (
    'baseboard-asset-tag',
    'baseboard-manufacturer',
    'baseboard-product-name',
    'baseboard-serial-number',
    'baseboard-version',
    'bios-release-date',
    'bios-vendor',
    'bios-version',
    'chassis-asset-tag',
    'chassis-manufacturer',
    'chassis-serial-number',
    'chassis-type',
    'chassis-version',
    'processor-family',
    'processor-frequency',
    'processor-manufacturer',
    'processor-version',
    'system-manufacturer',
    'system-product-name',
    'system-serial-number',
    'system-uuid',
    'system-version',
)

TABLES = {
    'system-uuid': {
        '00000000-0000-0000-0000-000000000001': 'koap1',
    },
    'baseboard-product-name': {
        'Z35FM': 'daru1',
        'Z35F': 'daru1',
        'MS-1221': 'daru2',
        'IFL91': 'panv3',
        'IFT01': 'gazv5',
        'IFT00': 'gazp5',
        'A8N8L': 'sabv1',
        'M2N8L': 'sabv2',
        'P5K-VM': 'sabv3',
        'IFL90': 'serp3',
        'JFL92': 'serp4',
        'MS-7250': 'wilp1',
        'A8V-MQ': 'ratv1',
        'P5VD2-MX': 'ratv2',
        'P5VD2-VM': 'ratv3',
        'D945GCPE': 'ratv4',
        'P5GC-MX/1333': 'ratv5',
        'MPAD-MSAE Customer Reference Boards': 'gazv2',
        'K8N-DL': 'wilp2',
        'KFN5-D SLI': 'wilp3',
        'DP35DP': 'wilp5',
    },
    'system-product-name': {
        'MS-1012': 'gazv1',
        'Z62FP': 'gazv3',
        'Z62FM': 'gazv4',
        'Z62F': 'gazp1',
        'Z62J': 'gazp2',
        'Z62JM': 'gazp3',
        'Z62JP': 'gazp3',
        'U-100': 'meec1',
        'Z96F': 'panv2',
        'Centoris V661': 'panv2',
        'Z96FM': 'panv2',
        'HEL80I': 'serp1',
        'HEL8X': 'serp1',
        'HEL80C': 'serp2',
        'UW1': 'star1',
        'star1': 'star1',
        'E10IS': 'star2',
        'E10IS2': 'star2',
        'Star2': 'star2',
        'A7V': 'bonp1',
        'M570TU': 'bonp2',
        'M720T/M730T': 'daru3',
        'M740T/M760T': 'panp4i',
        'M740TU/M760TU': 'panp4n',
        'M860TU': 'serp5',
    },
    'system-version': {
        'addw1': 'addw1',
        'addw2': 'addw2',
        'bonp2': 'bonp2',
        'bonp3': 'bonp3',
        'bonp4': 'bonp4',
        'bonp5': 'bonp5',
        'bonx6': 'bonx6',
        'bonx7': 'bonx7',
        'bonx8': 'bonx8',
        'bonw9': 'bonw9',
        'bonw10': 'bonw10',
        'bonw11': 'bonw11',
        'bonw12': 'bonw12',
        'bonw13': 'bonw13',
        'bonw14': 'bonw14',
        'darp5': 'darp5',
        'darp6': 'darp6',
        'darp7': 'darp7',
        'galu1': 'galu1',
        'galp2': 'galp2',
        'galp3': 'galp3',
        'galp3-b': 'galp3-b',
        'galp3-c': 'galp3-c',
        'galp4': 'galp4',
        'galp5': 'galp5',
        'gazu1': 'gazu1',
        'gazp6': 'gazp6',
        'gazp7': 'gazp7',
        'gazp8': 'gazp8',
        'gazp9': 'gazp9',
        'gazp9b': 'gazp9b',
        'gazp9c': 'gazp9c',
        'gaze10': 'gaze10',
        'gaze11': 'gaze11',
        'gaze12': 'gaze12',
        'gaze13': 'gaze13',
        'gaze14': 'gaze14',
        'gaze15': 'gaze15',
        'gaze16-3050': 'gaze16-3050',
        'gaze16-3060': 'gaze16-3060',
        'gaze16-3060-b': 'gaze16-3060-b',
        'daru3': 'daru3',
        'daru4': 'daru4',
        'kudp1': 'kudp1',
        'kudp1b': 'kudp1b',
        'kudp1c': 'kudp1c',
        'kudu2': 'kudu2',
        'kudu3': 'kudu3',
        'kudu4': 'kudu4',
        'kudu5': 'kudu5',
        'kudu6': 'kudu6',
        'panp4n': 'panp4n',
        'panp5': 'panp5',
        'panp6': 'panp6',
        'panp7': 'panp7',
        'panp8': 'panp8',
        'panp9': 'panp9',
        'pang10': 'pang10',
        'pang11': 'pang11',
        'lemu1': 'lemu1',
        'lemu2': 'lemu2',
        'lemu3': 'lemu3',
        'lemu4': 'lemu4',
        'lemu5': 'lemu5',
        'lemu6': 'lemu6',
        'lemu7': 'lemu7',
        'lemu8': 'lemu8',
        'lemp9': 'lemp9',
        'lemp10': 'lemp10',
        'leo1': 'leo1',
        'leox2': 'leox2',
        'leox3': 'leox3',
        'leox4': 'leox4',
        'leox5': 'leox5',
        'leow6': 'leow6',
        'leow7': 'leow7',
        'leow8': 'leow8',
        'leow9': 'leow9',
        'leow9-b': 'leow9-b',
        'leow9-w': 'leow9-w',
        'meer1': 'meer1',
        'meer2': 'meer2',
        'meer3': 'meer3',
        'meer4': 'meer4',
        'meer5': 'meer5',
        'meer6': 'meer6',
        'ment1': 'ment1',
        'ment2': 'ment2',
        'ment3': 'ment3',
        'ment5': 'ment5',
        'orxp1': 'orxp1',
        'oryp2': 'oryp2',
        'oryp2-ess': 'oryp2-ess',
        'oryp3': 'oryp3',
        'oryp3-ess': 'oryp3-ess',
        'oryp3-b': 'oryp3-b',
        'oryp4': 'oryp4',
        'oryp4-b': 'oryp4-b',
        'oryp5': 'oryp5',
        'oryp6': 'oryp6',
        'oryp7': 'oryp7',
        'oryp8': 'oryp8',
        'ratv6': 'ratv6',
        'ratu1': 'ratu1',
        'ratu2': 'ratu2',
        'ratp1': 'ratp1',
        'ratp2': 'ratp2',
        'ratp3': 'ratp3',
        'ratp4': 'ratp4',
        'ratp5': 'ratp5',
        'star3': 'star3',
        'star4': 'star4',
        'star5': 'star5',
        'thelio-b1': 'thelio-b1',
        'thelio-b2': 'thelio-b2',
        'thelio-r1': 'thelio-r1',
        'thelio-r2': 'thelio-r2',
        'thelio-major-b1': 'thelio-major-b1',
        'thelio-major-b1.1': 'thelio-major-b1.1',
        'thelio-major-b2': 'thelio-major-b2',
        'thelio-major-b3': 'thelio-major-b3',
        'thelio-major-r1': 'thelio-major-r1',
        'thelio-major-r2': 'thelio-major-r2',
        'thelio-major-r2.1': 'thelio-major-r2.1',
        'thelio-massive-b1': 'thelio-massive-b1',
        'thelio-mega-b1': 'thelio-mega-b1',
        'thelio-mega-r1': 'thelio-mega-r1',
        'thelio-mega-r1.1': 'thelio-mega-r1.1',
        'thelio-mira-b1': 'thelio-mira-b1',
        'thelio-mira-r1': 'thelio-mira-r1',
        'wilb1': 'wilb1',
        'wilb2': 'wilb2',
        'wilp6': 'wilp6',
        'wilp7': 'wilp7',
        'wilp8': 'wilp8',
        'wilp9': 'wilp9',
        'wilp10': 'wilp10',
        'wilp11': 'wilp11',
        'wilp12': 'wilp12',
        'wilp13': 'wilp13',
        'wilp14': 'wilp14',
        'serp5': 'serp5',
        'serp6': 'serp6',
        'serp7': 'serp7',
        'serw8-15': 'serw8-15',
        'serw8-17': 'serw8-17',
        'serw8-17g': 'serw8-17g',
        'serw9': 'serw9',
        'serw10': 'serw10',
        'serw11': 'serw11',
        'serw11-b': 'serw11-b',
        'serw12': 'serw12',
        'silw1': 'silw1',
        'silw2': 'silw2',
        'silw3': 'silw3',
        'sabc1': 'sabc1',
        'sabc2': 'sabc2',
        'sabc3': 'sabc3',
        'sabl4': 'sabl4',
        'sabl5': 'sabl5',
        'sabl6': 'sabl6',
        'sabt1': 'sabt1',
        'sabt2': 'sabt2',
        'sabt3': 'sabt3',
    },
}


def dmidecode(keyword):
    cmd = ['dmidecode', '-s', keyword]
    return SubProcess.check_output(cmd).decode('utf-8').strip()


def get_dmi_info():
    return dict(
        (keyword, dmidecode(keyword)) for keyword in KEYWORDS
    )


def get_all_dmi_info():
    return dict(
        (keyword, dmidecode(keyword)) for keyword in ALL_KEYWORDS
    )


def determine_model(info=None):
    """
    Determine the System76 model number.
    """
    if info is None:
        info = get_dmi_info()
    for keyword in KEYWORDS:
        value = info[keyword]
        table = TABLES[keyword]
        if value in table:
            return table[value]
    return 'nonsystem76'


def determine_model_new(sysdir='/sys', info=None):
    model = read_dmi_id('product_version', sysdir)
    if model in TABLES['system-version']:
        return model
    return determine_model(info)
