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


PRODUCTS = {
    # Bonobo:
    'bonp1': {'name': 'Bonobo Performance'},
    'bonp2': {'name': 'Bonobo Performance'},
    'bonp3': {'name': 'Bonobo Performance'},
    'bonp4': {'name': 'Bonobo Performance'},
    'bonp5': {'name': 'Bonobo Performance'},
    'bonx6': {'name': 'Bonobo Extreme'},

    # Darter:
    'daru1': {'name': 'Darter Ultra'},
    'daru2': {'name': 'Darter Ultra'},
    'daru3': {'name': 'Darter Ultra'},

    # Gazelle:
    'gazp1': {'name': 'Gazelle Performance'},
    'gazp2': {'name': 'Gazelle Performance'},
    'gazp3': {'name': 'Gazelle Performance'},
    'gazp5': {'name': 'Gazelle Value with nVidia and Camera'},
    'gazp6': {'name': 'Gazelle Professional'},
    'gazp7': {'name': 'Gazelle Professional'},
    'gazp8': {'name': 'Gazelle Professional'},
    'gazu1': {'name': 'Gazelle Ultra'},
    'gazv1': {'name': 'Gazelle Value'},
    'gazv2': {'name': 'Gazelle Value'},
    'gazv3': {'name': 'Gazelle Value'},
    'gazv4': {'name': 'Gazelle Value'},
    'gazv5': {'name': 'Gazelle Value'},

    # Koala:  
    'koap1': {'name': 'Koala Performance'},

    # Lemur:
    'lemu1': {'name': 'Lemur UltraThin'},
    'lemu2': {'name': 'Lemur UltraThin'},
    'lemu3': {'name': 'Lemur UltraThin'},
    'lemu4': {'name': 'Lemur UltraThin'},

    # Leopard:
    'leo1': {'name': 'The Leopard Extreme'},
    'leox2': {'name': 'The Leopard Extreme'},
    'leox3': {'name': 'The Leopard Extreme'},

    # Meerkat:
    'meec1': {'name': 'Meerkat Compact'},
    'ment1': {'name': 'Meerkat NetTop'},
    'ment2': {'name': 'Meerkat Ion NetTop'},
    'ment3': {'name': 'Meerkat NetTop'},
    'ment5': {'name': 'Meerkat Ion NetTop'},

    # Pangolin:
    'panp4i': {'name': 'Pangolin Performance'},
    'panp4n': {'name': 'Pangolin Performance'},
    'panp5': {'name': 'Pangolin Performance'},
    'panp6': {'name': 'Pangolin Performance'},
    'panp7': {'name': 'Pangolin Performance'},
    'panp8': {'name': 'Pangolin Performance'},
    'panp9': {'name': 'Pangolin Performance'},
    #'panv1': {'name': 'Pangolin Value'},  # FIXME: Not in model.py
    'panv2': {'name': 'Pangolin Value'},
    'panv3': {'name': 'Pangolin Value'},

    # Ratel:
    'ratp1': {'name': 'Ratel Performance'},
    'ratu1': {'name': 'Ratel Ultra'},
    'ratu2': {'name': 'Ratel Ultra'},
    'ratv1': {'name': 'Ratel Value'},
    'ratv2': {'name': 'Ratel Value'},
    'ratv3': {'name': 'Ratel Value'},
    'ratv4': {'name': 'Ratel Value'},
    'ratv5': {'name': 'Ratel Value'},
    'ratv6': {'name': 'Ratel Value'},

    # Sable:
    'sabc1': {'name': 'Sable Complete'},
    'sabv1': {'name': 'Sable Series'},
    'sabv2': {'name': 'Sable Series'},
    'sabv3': {'name': 'Sable Series'},

    # Serval:
    'serp1': {'name': 'Serval Performance'},
    'serp2': {'name': 'Serval Performance'},
    'serp3': {'name': 'Serval Performance'},
    'serp4': {'name': 'Serval Performance'},
    'serp5': {'name': 'Serval Performance'},
    'serp6': {'name': 'Serval Performance'},
    'serp7': {'name': 'Serval Performance'},

    # Starling:
    'star1': {'name': 'Starling NetBook'},
    'star2': {'name': 'Starling EduBook'},
    'star3': {'name': 'Starling NetBook'},
    'star4': {'name': 'Starling NetBook'},
    'star5': {'name': 'Starling NetBook'},

    # Wildebeest:
    'wilb1': {'name': 'Wildebeest Performance'},
    'wilb2': {'name': 'Wildebeest Performance'},

    # Wild Dog:
    'wilp1': {'name': 'Wild Dog Performance'},
    'wilp2': {'name': 'Wild Dog Performance'},
    'wilp3': {'name': 'Wild Dog Performance'},
    # FIXME: Make sure there was no wilp4
    'wilp5': {'name': 'Wild Dog Performance'},
    'wilp6': {'name': 'Wild Dog Performance'},
    'wilp7': {'name': 'Wild Dog Performance'},
    'wilp8': {'name': 'Wild Dog Performance'},
    'wilp9': {'name': 'Wild Dog Performance'},
}
