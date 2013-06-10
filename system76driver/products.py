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
Map product name to list of driver actions.
"""

from . import actions


PRODUCTS = {
    # Bonobo:
    'bonp1': {'name': 'Bonobo Performance', 'drivers': [], 'defaults': []},
    'bonp2': {'name': 'Bonobo Performance', 'drivers': [], 'defaults': []},
    'bonp3': {'name': 'Bonobo Performance', 'drivers': [], 'defaults': []},
    'bonp4': {'name': 'Bonobo Professional', 'drivers': [], 'defaults': []},
    'bonp5': {'name': 'Bonobo Professional', 'drivers': [], 'defaults': []},
    'bonx6': {'name': 'Bonobo Extreme',
        'drivers': [
            actions.fingerprintGUI,
            actions.plymouth1080,
            actions.wifi_pm_disable,
        ],
        'defaults': []
    },

    # Darter:
    'daru1': {'name': 'Darter Ultra', 'drivers': [], 'defaults': []},
    'daru2': {'name': 'Darter Ultra', 'drivers': [], 'defaults': []},
    'daru3': {'name': 'Darter Ultra', 'drivers': [], 'defaults': []},

    # Gazelle:
    'gazp1': {'name': 'Gazelle Performance', 'drivers': [], 'defaults': []},
    'gazp2': {'name': 'Gazelle Performance', 'drivers': [], 'defaults': []},
    'gazp3': {'name': 'Gazelle Performance', 'drivers': [], 'defaults': []},
    'gazp5': {'name': 'Gazelle Value with nVidia and Camera',
        'drivers': [],
        'defaults': [],
    },
    'gazp6': {'name': 'Gazelle Professional', 'drivers': [], 'defaults': []},
    'gazp7': {'name': 'Gazelle Professional', 'drivers': [], 'defaults': []},
    'gazp8': {'name': 'Gazelle Professional', 'drivers': [], 'defaults': []},
    'gazu1': {'name': 'Gazelle Ultra', 'drivers': [], 'defaults': []},
    'gazv1': {'name': 'Gazelle Value', 'drivers': [], 'defaults': []},
    'gazv2': {'name': 'Gazelle Value', 'drivers': [], 'defaults': []},
    'gazv3': {'name': 'Gazelle Value', 'drivers': [], 'defaults': []},
    'gazv4': {'name': 'Gazelle Value', 'drivers': [], 'defaults': []},
    'gazv5': {'name': 'Gazelle Value', 'drivers': [], 'defaults': []},

    # Koala:  
    'koap1': {'name': 'Koala Performance', 'drivers': [], 'defaults': []},

    # Lemur:
    'lemu1': {'name': 'Lemur UltraThin', 'drivers': [], 'defaults': []},
    'lemu2': {'name': 'Lemur UltraThin', 'drivers': [], 'defaults': []},
    'lemu3': {'name': 'Lemur Ultra', 'drivers': [], 'defaults': []},
    'lemu4': {'name': 'Lemur Ultra', 'drivers': [], 'defaults': []},

    # Leopard:
    'leo1': {'name': 'The Leopard Extreme', 'drivers': [], 'defaults': []},
    'leox2': {'name': 'The Leopard Extreme', 'drivers': [], 'defaults': []},
    'leox3': {'name': 'The Leopard Extreme', 'drivers': [], 'defaults': []},

    # Meerkat:
    'meec1': {'name': 'Meerkat Compact', 'drivers': [], 'defaults': []},
    'ment1': {'name': 'Meerkat NetTop', 'drivers': [], 'defaults': []},
    'ment2': {'name': 'Meerkat Ion NetTop', 'drivers': [], 'defaults': []},
    'ment3': {'name': 'Meerkat NetTop', 'drivers': [], 'defaults': []},
    'ment5': {'name': 'Meerkat Ion NetTop', 'drivers': [], 'defaults': []},

    # Pangolin:
    'panp4i': {'name': 'Pangolin Performance', 'drivers': [], 'defaults': []},
    'panp4n': {'name': 'Pangolin Performance', 'drivers': [], 'defaults': []},
    'panp5': {'name': 'Pangolin Performance', 'drivers': [], 'defaults': []},
    'panp6': {'name': 'Pangolin Performance', 'drivers': [], 'defaults': []},
    'panp7': {'name': 'Pangolin Performance', 'drivers': [], 'defaults': []},
    'panp8': {'name': 'Pangolin Performance', 'drivers': [], 'defaults': []},
    'panp9': {'name': 'Pangolin Performance', 'drivers': [], 'defaults': []},
    #'panv1': {'name': 'Pangolin Value'},  # FIXME: Not in model.py
    'panv2': {'name': 'Pangolin Value', 'drivers': [], 'defaults': []},
    'panv3': {'name': 'Pangolin Value', 'drivers': [], 'defaults': []},

    # Ratel:
    'ratp1': {'name': 'Ratel Performance', 'drivers': [], 'defaults': []},
    'ratu1': {'name': 'Ratel Ultra', 'drivers': [], 'defaults': []},
    'ratu2': {'name': 'Ratel Ultra', 'drivers': [], 'defaults': []},
    'ratv1': {'name': 'Ratel Value', 'drivers': [], 'defaults': []},
    'ratv2': {'name': 'Ratel Value', 'drivers': [], 'defaults': []},
    'ratv3': {'name': 'Ratel Value', 'drivers': [], 'defaults': []},
    'ratv4': {'name': 'Ratel Value', 'drivers': [], 'defaults': []},
    'ratv5': {'name': 'Ratel Value', 'drivers': [], 'defaults': []},
    'ratv6': {'name': 'Ratel Value', 'drivers': [], 'defaults': []},

    # Sable:
    'sabc1': {'name': 'Sable Complete', 'drivers': [], 'defaults': []},
    'sabv1': {'name': 'Sable Series', 'drivers': [], 'defaults': []},
    'sabv2': {'name': 'Sable Series', 'drivers': [], 'defaults': []},
    'sabv3': {'name': 'Sable Series', 'drivers': [], 'defaults': []},

    # Serval:
    'serp1': {'name': 'Serval Performance', 'drivers': [], 'defaults': []},
    'serp2': {'name': 'Serval Performance', 'drivers': [], 'defaults': []},
    'serp3': {'name': 'Serval Performance', 'drivers': [], 'defaults': []},
    'serp4': {'name': 'Serval Performance', 'drivers': [], 'defaults': []},
    'serp5': {'name': 'Serval Professional', 'drivers': [], 'defaults': []},
    'serp6': {'name': 'Serval Professional', 'drivers': [], 'defaults': []},
    'serp7': {'name': 'Serval Professional', 'drivers': [], 'defaults': []},

    # Starling:
    'star1': {'name': 'Starling NetBook', 'drivers': [], 'defaults': []},
    'star2': {'name': 'Starling EduBook', 'drivers': [], 'defaults': []},
    'star3': {'name': 'Starling NetBook', 'drivers': [], 'defaults': []},
    'star4': {'name': 'Starling NetBook', 'drivers': [], 'defaults': []},
    'star5': {'name': 'Starling NetBook', 'drivers': [], 'defaults': []},

    # Wildebeest:
    'wilb1': {'name': 'Wildebeest Performance', 'drivers': [], 'defaults': []},
    'wilb2': {'name': 'Wildebeest Performance', 'drivers': [], 'defaults': []},

    # Wild Dog:
    'wilp1': {'name': 'Wild Dog Performance', 'drivers': [], 'defaults': []},
    'wilp2': {'name': 'Wild Dog Performance', 'drivers': [], 'defaults': []},
    'wilp3': {'name': 'Wild Dog Performance', 'drivers': [], 'defaults': []},
    'wilp5': {'name': 'Wild Dog Performance', 'drivers': [], 'defaults': []},
    'wilp6': {'name': 'Wild Dog Performance', 'drivers': [], 'defaults': []},
    'wilp7': {'name': 'Wild Dog Performance', 'drivers': [], 'defaults': []},
    'wilp8': {'name': 'Wild Dog Performance', 'drivers': [], 'defaults': []},
    'wilp9': {'name': 'Wild Dog Performance', 'drivers': [], 'defaults': []},
}
