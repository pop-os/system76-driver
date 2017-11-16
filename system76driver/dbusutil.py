# system76-driver: Universal driver for System76 computers
# Copyright (C) 2005-2017 System76, Inc.
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
DBus utility functions for the hidpi daemon.  On Gnome we need to talk to Mutter over its dbus api to set scaling on nvidia systems.
"""

from gi.repository import Gio, GLib


def dbus_helper(destination = 'org.gnome.Mutter.DisplayConfig',
                path        = '/org/gnome/Mutter/DisplayConfig',
                interface   = 'org.gnome.Mutter.DisplayConfig',
                method      = None,
                args        = None,
                answer_fmt  = None,
                proxy_prpty = Gio.DBusCallFlags.NONE,
                timeout     = -1,
                cancellable = None 
                ):
    
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    reply = bus.call_sync(destination, path, interface,
                      method, args, answer_fmt,
                      proxy_prpty, timeout, cancellable)
    return reply

def unpack_current_state(current_state):
    configuration_serial = current_state[0]
    monitors = current_state[1]
    log_displays = current_state[2]
    logical_displays = []
    for log_display in log_displays:
        processed_displays = []
        logical_display = { 'x_position' : log_display[0],
                            'y_position' : log_display[1],
                            'scale'      : log_display[2],
                            'transform'  : log_display[3],
                            'primary'    : log_display[4]
                          }
        #logical_displays.append(logical_display)
        log_monitors = log_display[5]
        processed_monitors = []
        for monitor in log_monitors:
            processed_monitor = {}
            processed_monitor['connector'] = monitor[0]
            processed_monitor['vendor']    = monitor[1]
            processed_monitor['product']   = monitor[2]
            processed_monitor['serial']    = monitor[3]
            for mon in monitors:
                if mon[0][0] == monitor[0]:
                    processed_monitor['modes'] = mon[1]
                    #print(processed_monitor)
            processed_monitors.append(processed_monitor)
        logical_display['monitors'] = processed_monitors
        logical_displays.append(logical_display)
        #print(logical_displays)
    return configuration_serial, logical_displays

def get_current_state():
    current_state = dbus_helper(method='GetCurrentState', 
                                answer_fmt  = GLib.VariantType.new ('(ua((ssss)a(siiddada{sv})a{sv})a(iiduba(ssss)a{sv})a{sv})')
    )
    #print(current_state.unpack())
    
    return unpack_current_state(current_state)
    
def apply_monitors_configuration(configuration_serial, displays, scale):
    displays_arg = []
    
    #print(displays)
    for display in displays:
        #print("display")
        #generate monitors argument for each display
        monitors_arg = []
        display_scale = scale
        for monitor in display['monitors']:
            monitors_arg.append(( 
                        monitor['connector'], 
                        monitor['modes'][0][0], 
                        {
                            'underscanning': GLib.Variant('b', False)
                        }
                    ))
            if scale not in monitor['modes'][0][5]:
                display_scale = 1.0
        display_arg = (
                    display['x_position'], 
                    display['y_position'], 
                    display_scale, 
                    display['transform'], 
                    display['primary'], 
                    monitors_arg, 
                )
        displays_arg.append(display_arg)
    #print(displays_arg)
    args = GLib.Variant('(uua(iiduba(ssa{sv}))a{sv})', ( configuration_serial, 1,
            displays_arg,
                {
                },
            )
            )
    #print(args)
    dbus_helper(method='ApplyMonitorsConfig',
                    args = args)

def get_scale():
    configuration_serial, displays = get_current_state()
    scale = 1.0
    for display in displays:
        if display['scale'] > scale:
            scale = display['scale']
    return scale

def set_scale(scale):
    configuration_serial, displays = get_current_state()
    apply_monitors_configuration(configuration_serial, displays, scale)
    
#set_scale(2.0)
