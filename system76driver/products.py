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
Map model name to list of driver actions.
"""

from . import actions


PRODUCTS = {
    # Bonobo:
    'bonp1': {
        'name': 'Bonobo Performance',
        'drivers': [],
    },
    'bonp2': {
        'name': 'Bonobo Performance',
        'drivers': [],
    },
    'bonp3': {
        'name': 'Bonobo Performance',
        'drivers': [],
    },
    'bonp4': {
        'name': 'Bonobo Professional',
        'drivers': [],
    },
    'bonp5': {
        'name': 'Bonobo Professional',
        'drivers': [],
    },
    'bonx6': {
        'name': 'Bonobo Extreme',
        'drivers': [
            actions.plymouth1080,
            actions.wifi_pm_disable,
        ],
    },
    'bonx7': {
        'name': 'Bonobo Extreme',
        'drivers': [
            #actions.plymouth1080,  # Causes problems with nvidia-313-updates
            actions.wifi_pm_disable,
            actions.bonx7_icc,
        ],
        'screens': {
            'c73b258ef528c02b30beb0c8a35ef93c': 'matte',
            'feeb71dac035e4d9184b0c39ca189eb4': 'glossy',
            
        }
    },

    # Darter:
    'daru1': {
        'name': 'Darter Ultra',
        'drivers': [],
    },
    'daru2': {
        'name': 'Darter Ultra',
        'drivers': [],
    },
    'daru3': {
        'name': 'Darter Ultra',
        'drivers': [],
    },
    'daru4': {
        'name': 'Darter UltraThin',
        'drivers': [
            actions.backlight_vendor,
            actions.internal_mic_gain,
        ],
    },

    # Galago:
    'galu1': {
        'name': 'Galago UltraPro',
        'drivers': [
            actions.wifi_pm_disable,
            actions.internal_mic_gain,
            actions.galu1_icc,
        ],
        'screens': {
            '1fcfbf3269ba92bdeb2f8a009f7894ef': 'IPS matte ColorPro',
        }
    },

    # Gazelle:
    'gazp1': {
        'name': 'Gazelle Performance',
        'drivers': [],
    },
    'gazp2': {
        'name': 'Gazelle Performance',
        'drivers': [],
    },
    'gazp3': {
        'name': 'Gazelle Performance',
        'drivers': [],
    },
    'gazp5': {
        'name': 'Gazelle Value with nVidia and Camera',
        'drivers': [],
    },
    'gazp6': {
        'name': 'Gazelle Professional',
        'drivers': [],
    },
    'gazp7': {
        'name': 'Gazelle Professional',
        'drivers': [
            actions.lemu1,
            actions.wifi_pm_disable,
        ],
    },
    'gazp8': {
        'name': 'Gazelle Professional',
        'drivers': [
            actions.lemu1,
            actions.wifi_pm_disable,
        ],
    },
    'gazp9': {
        'name': 'Gazelle Professional',
        'drivers': [
            actions.backlight_vendor,
            actions.wifi_pm_disable,
            actions.gazp9_icc,
        ],
        'screens': {
            '38306ee6ae5ccf81d2951aa95ae823f4': 'system76-gazp9-glossy.icc',
            '6c4c6b27d0a90b99322e487510455230': 'system76-gazp9-ips-matte.icc',
        },
    },
    'gazu1': {
        'name': 'Gazelle Ultra',
        'drivers': [
            actions.uvcquirks,
        ],
    },
    'gazv1': {
        'name': 'Gazelle Value',
        'drivers': [],
    },
    'gazv2': {
        'name': 'Gazelle Value',
        'drivers': [],
    },
    'gazv3': {
        'name': 'Gazelle Value',
        'drivers': [],
    },
    'gazv4': {
        'name': 'Gazelle Value',
        'drivers': [],
    },
    'gazv5': {
        'name': 'Gazelle Value',
        'drivers': [],
    },

    # Koala:  
    'koap1': {
        'name': 'Koala Performance',
        'drivers': [],
    },

    # Kudu:  
    'kudp1': {
        'name': 'Kudu Professional',
        'drivers': [],
    },

    # Lemur:
    'lemu1': {
        'name': 'Lemur UltraThin',
        'drivers': [],
    },
    'lemu2': {
        'name': 'Lemur UltraThin',
        'drivers': [],
    },
    'lemu3': {
        'name': 'Lemur Ultra',
        'drivers': [],
    },
    'lemu4': {
        'name': 'Lemur Ultra',
        'drivers': [
            actions.wifi_pm_disable,
            actions.lemu1,
        ],
    },

    # Leopard:
    'leo1': {
        'name': 'The Leopard Extreme',
        'drivers': [],
    },
    'leox2': {
        'name': 'The Leopard Extreme',
        'drivers': [],
    },
    'leox3': {
        'name': 'The Leopard Extreme',
        'drivers': [],
    },
    'leox4': {
        'name': 'The Leopard Extreme',
        'drivers': [],
    },

    # Meerkat:
    'meec1': {
        'name': 'Meerkat Compact',
        'drivers': [],
    },
    'ment1': {
        'name': 'Meerkat NetTop',
        'drivers': [],
    },
    'ment2': {
        'name': 'Meerkat Ion NetTop',
        'drivers': [],
    },
    'ment3': {
        'name': 'Meerkat NetTop',
        'drivers': [],
    },
    'ment5': {
        'name': 'Meerkat Ion NetTop',
        'drivers': [],
    },

    # Pangolin:
    'panp4i': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp4n': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp5': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp6': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp7': {
        'name': 'Pangolin Performance',
        'drivers': [
            actions.radeon_dpm,
        ],
    },
    'panp8': {
        'name': 'Pangolin Performance',
        'drivers': [],
    },
    'panp9': {
        'name': 'Pangolin Performance',
        'drivers': [
            actions.wifi_pm_disable,
            actions.lemu1,
        ],
    },
    #'panv1': {'name': 'Pangolin Value'},  # FIXME: Not in model.py
    'panv2': {
        'name': 'Pangolin Value',
        'drivers': [],
    },
    'panv3': {
        'name': 'Pangolin Value',
        'drivers': [],
    },

    # Ratel:
    'ratp1': {
        'name': 'Ratel Performance',
        'drivers': [],
    },
    'ratp2': {
        'name': 'Ratel Performance',
        'drivers': [],
    },
    'ratu1': {
        'name': 'Ratel Ultra',
        'drivers': [],
    },
    'ratu2': {
        'name': 'Ratel Ultra',
        'drivers': [],
    },
    'ratv1': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv2': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv3': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv4': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv5': {
        'name': 'Ratel Value',
        'drivers': [],
    },
    'ratv6': {
        'name': 'Ratel Value',
        'drivers': [],
    },

    # Sable:
    'sabc1': {
        'name': 'Sable Complete',
        'drivers': [],
    },
    'sabv1': {
        'name': 'Sable Series',
        'drivers': [],
    },
    'sabv2': {
        'name': 'Sable Series',
        'drivers': [],
    },
    'sabv3': {
        'name': 'Sable Series',
        'drivers': [],
    },

    # Serval:
    'serp1': {
        'name': 'Serval Performance',
        'drivers': [],
    },
    'serp2': {
        'name': 'Serval Performance',
        'drivers': [],
    },
    'serp3': {
        'name': 'Serval Performance',
        'drivers': [],
    },
    'serp4': {
        'name': 'Serval Performance',
        'drivers': [],
    },
    'serp5': {
        'name': 'Serval Professional',
        'drivers': [],
    },
    'serp6': {
        'name': 'Serval Professional',
        'drivers': [],
    },
    'serp7': {
        'name': 'Serval Professional',
        'drivers': [],
    },

    # Starling:
    'star1': {
        'name': 'Starling NetBook',
        'drivers': [],
    },
    'star2': {
        'name': 'Starling EduBook',
        'drivers': [],
    },
    'star3': {
        'name': 'Starling NetBook',
        'drivers': [],
    },
    'star4': {
        'name': 'Starling NetBook',
        'drivers': [],
    },
    'star5': {
        'name': 'Starling NetBook',
        'drivers': [],
    },

    # Wildebeest:
    'wilb1': {
        'name': 'Wildebeest Performance',
        'drivers': [],
    },
    'wilb2': {
        'name': 'Wildebeest Performance',
        'drivers': [],
    },

    # Wild Dog:
    'wilp1': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp2': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp3': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp5': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp6': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp7': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp8': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp9': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
    'wilp10': {
        'name': 'Wild Dog Performance',
        'drivers': [],
    },
}
