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
        'prefs': [],
    },
    'bonp2': {
        'name': 'Bonobo Performance',
        'drivers': [],
        'prefs': [],
    },
    'bonp3': {
        'name': 'Bonobo Performance',
        'drivers': [],
        'prefs': [],
    },
    'bonp4': {
        'name': 'Bonobo Professional',
        'drivers': [],
        'prefs': [],
    },
    'bonp5': {
        'name': 'Bonobo Professional',
        'drivers': [],
        'prefs': [],
    },
    'bonx6': {
        'name': 'Bonobo Extreme',
        'drivers': [
            actions.fingerprintGUI,
            actions.plymouth1080,
            actions.wifi_pm_disable,
        ],
        'prefs': [],
    },

    # Darter:
    'daru1': {
        'name': 'Darter Ultra',
        'drivers': [],
        'prefs': [],
    },
    'daru2': {
        'name': 'Darter Ultra',
        'drivers': [],
        'prefs': [],
    },
    'daru3': {
        'name': 'Darter Ultra',
        'drivers': [],
        'prefs': [],
    },

    # Gazelle:
    'gazp1': {
        'name': 'Gazelle Performance',
        'drivers': [],
        'prefs': [],
    },
    'gazp2': {
        'name': 'Gazelle Performance',
        'drivers': [],
        'prefs': [],
    },
    'gazp3': {
        'name': 'Gazelle Performance',
        'drivers': [],
        'prefs': [],
    },
    'gazp5': {
        'name': 'Gazelle Value with nVidia and Camera',
        'drivers': [],
        'prefs': [],
    },
    'gazp6': {
        'name': 'Gazelle Professional',
        'drivers': [],
        'prefs': [],
    },
    'gazp7': {
        'name': 'Gazelle Professional',
        'drivers': [],
        'prefs': [],
    },
    'gazp8': {
        'name': 'Gazelle Professional',
        'drivers': [],
        'prefs': [],
    },
    'gazp9': {
        'name': 'Gazelle Professional',
        'drivers': [
            actions.airplane_mode,
            actions.backlight_vendor,
        ],
        'prefs': [],
    },
    'gazu1': {
        'name': 'Gazelle Ultra',
        'drivers': [],
        'prefs': [],
    },
    'gazv1': {
        'name': 'Gazelle Value',
        'drivers': [],
        'prefs': [],
    },
    'gazv2': {
        'name': 'Gazelle Value',
        'drivers': [],
        'prefs': [],
    },
    'gazv3': {
        'name': 'Gazelle Value',
        'drivers': [],
        'prefs': [],
    },
    'gazv4': {
        'name': 'Gazelle Value',
        'drivers': [],
        'prefs': [],
    },
    'gazv5': {
        'name': 'Gazelle Value',
        'drivers': [],
        'prefs': [],
    },

    # Koala:  
    'koap1': {
        'name': 'Koala Performance',
        'drivers': [],
        'prefs': [],
    },

    # Lemur:
    'lemu1': {
        'name': 'Lemur UltraThin',
        'drivers': [],
        'prefs': [],
    },
    'lemu2': {
        'name': 'Lemur UltraThin',
        'drivers': [],
        'prefs': [],
    },
    'lemu3': {
        'name': 'Lemur Ultra',
        'drivers': [],
        'prefs': [],
    },
    'lemu4': {
        'name': 'Lemur Ultra',
        'drivers': [
            actions.wifi_pm_disable,
            actions.lemu1,
        ],
        'prefs': [],
    },

    # Leopard:
    'leo1': {
        'name': 'The Leopard Extreme',
        'drivers': [],
        'prefs': [],
    },
    'leox2': {
        'name': 'The Leopard Extreme',
        'drivers': [],
        'prefs': [],
    },
    'leox3': {
        'name': 'The Leopard Extreme',
        'drivers': [],
        'prefs': [],
    },

    # Meerkat:
    'meec1': {
        'name': 'Meerkat Compact',
        'drivers': [],
        'prefs': [],
    },
    'ment1': {
        'name': 'Meerkat NetTop',
        'drivers': [],
        'prefs': [],
    },
    'ment2': {
        'name': 'Meerkat Ion NetTop',
        'drivers': [],
        'prefs': [],
    },
    'ment3': {
        'name': 'Meerkat NetTop',
        'drivers': [],
        'prefs': [],
    },
    'ment5': {
        'name': 'Meerkat Ion NetTop',
        'drivers': [],
        'prefs': [],
    },

    # Pangolin:
    'panp4i': {
        'name': 'Pangolin Performance',
        'drivers': [],
        'prefs': [],
    },
    'panp4n': {
        'name': 'Pangolin Performance',
        'drivers': [],
        'prefs': [],
    },
    'panp5': {
        'name': 'Pangolin Performance',
        'drivers': [],
        'prefs': [],
    },
    'panp6': {
        'name': 'Pangolin Performance',
        'drivers': [],
        'prefs': [],
    },
    'panp7': {
        'name': 'Pangolin Performance',
        'drivers': [],
        'prefs': [],
    },
    'panp8': {
        'name': 'Pangolin Performance',
        'drivers': [],
        'prefs': [],
    },
    'panp9': {
        'name': 'Pangolin Performance',
        'drivers': [
            actions.wifi_pm_disable,
            actions.lemu1,
        ],
        'prefs': [],
    },
    #'panv1': {'name': 'Pangolin Value'},  # FIXME: Not in model.py
    'panv2': {
        'name': 'Pangolin Value',
        'drivers': [],
        'prefs': [],
    },
    'panv3': {
        'name': 'Pangolin Value',
        'drivers': [],
        'prefs': [],
    },

    # Ratel:
    'ratp1': {
        'name': 'Ratel Performance',
        'drivers': [],
        'prefs': [],
    },
    'ratu1': {
        'name': 'Ratel Ultra',
        'drivers': [],
        'prefs': [],
    },
    'ratu2': {
        'name': 'Ratel Ultra',
        'drivers': [],
        'prefs': [],
    },
    'ratv1': {
        'name': 'Ratel Value',
        'drivers': [],
        'prefs': [],
    },
    'ratv2': {
        'name': 'Ratel Value',
        'drivers': [],
        'prefs': [],
    },
    'ratv3': {
        'name': 'Ratel Value',
        'drivers': [],
        'prefs': [],
    },
    'ratv4': {
        'name': 'Ratel Value',
        'drivers': [],
        'prefs': [],
    },
    'ratv5': {
        'name': 'Ratel Value',
        'drivers': [],
        'prefs': [],
    },
    'ratv6': {
        'name': 'Ratel Value',
        'drivers': [],
        'prefs': [],
    },

    # Sable:
    'sabc1': {
        'name': 'Sable Complete',
        'drivers': [],
        'prefs': [],
    },
    'sabv1': {
        'name': 'Sable Series',
        'drivers': [],
        'prefs': [],
    },
    'sabv2': {
        'name': 'Sable Series',
        'drivers': [],
        'prefs': [],
    },
    'sabv3': {
        'name': 'Sable Series',
        'drivers': [],
        'prefs': [],
    },

    # Serval:
    'serp1': {
        'name': 'Serval Performance',
        'drivers': [],
        'prefs': [],
    },
    'serp2': {
        'name': 'Serval Performance',
        'drivers': [],
        'prefs': [],
    },
    'serp3': {
        'name': 'Serval Performance',
        'drivers': [],
        'prefs': [],
    },
    'serp4': {
        'name': 'Serval Performance',
        'drivers': [],
        'prefs': [],
    },
    'serp5': {
        'name': 'Serval Professional',
        'drivers': [],
        'prefs': [],
    },
    'serp6': {
        'name': 'Serval Professional',
        'drivers': [],
        'prefs': [],
    },
    'serp7': {
        'name': 'Serval Professional',
        'drivers': [],
        'prefs': [],
    },

    # Starling:
    'star1': {
        'name': 'Starling NetBook',
        'drivers': [],
        'prefs': [],
    },
    'star2': {
        'name': 'Starling EduBook',
        'drivers': [],
        'prefs': [],
    },
    'star3': {
        'name': 'Starling NetBook',
        'drivers': [],
        'prefs': [],
    },
    'star4': {
        'name': 'Starling NetBook',
        'drivers': [],
        'prefs': [],
    },
    'star5': {
        'name': 'Starling NetBook',
        'drivers': [],
        'prefs': [],
    },

    # Wildebeest:
    'wilb1': {
        'name': 'Wildebeest Performance',
        'drivers': [],
        'prefs': [],
    },
    'wilb2': {
        'name': 'Wildebeest Performance',
        'drivers': [],
        'prefs': [],
    },

    # Wild Dog:
    'wilp1': {
        'name': 'Wild Dog Performance',
        'drivers': [],
        'prefs': [],
    },
    'wilp2': {
        'name': 'Wild Dog Performance',
        'drivers': [],
        'prefs': [],
    },
    'wilp3': {
        'name': 'Wild Dog Performance',
        'drivers': [],
        'prefs': [],
    },
    'wilp5': {
        'name': 'Wild Dog Performance',
        'drivers': [],
        'prefs': [],
    },
    'wilp6': {
        'name': 'Wild Dog Performance',
        'drivers': [],
        'prefs': [],
    },
    'wilp7': {
        'name': 'Wild Dog Performance',
        'drivers': [],
        'prefs': [],
    },
    'wilp8': {
        'name': 'Wild Dog Performance',
        'drivers': [],
        'prefs': [],
    },
    'wilp9': {
        'name': 'Wild Dog Performance',
        'drivers': [],
        'prefs': [],
    },
}
