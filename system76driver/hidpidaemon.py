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
Daemon to set hidpi scaling/resolution for multi-display mixed-dpi scenarios.
Must run as regular user to correctly interface with gsettings.
"""

import logging
import re
import time

import threading

from collections import namedtuple

from gi.repository import Gtk

from gi.repository import GLib

from gi.repository import GObject

from .mockable import SubProcess
import subprocess


log = logging.getLogger(__name__)

NEEDS_HOTPLUG_AUTOSCALING = (
    'bonw12',
    'galp2',
    'oryp2-ess',
    'oryp3-ess',
    'serw10',
)

NVIDIA = {
    'bonw12',
    'oryp2-ess',
    'oryp3-ess',
    'serw10',
}

INTEL = {
    'galp2',
}

MODEL_MODES = {
    'galp2': '1600x900  118.25  1600 1696 1856 2112  900 903 908 934 -hsync +vsync',
}

GObject.threads_init()

XSize = namedtuple('XSize', ['width', 'height'])
XRes = namedtuple('XRes', ['x', 'y'])
XPanning = namedtuple('XPanning', ['res_x', 'res_y', 'pos_x', 'pos_y'])
XDisplay = namedtuple('XDisplay', ['display', 'size', 'panning', 'modes'])


class HotplugDialog(Gtk.MessageDialog):
    def __init__(self, parent, model):
        #TODO: Translatable strings
        Gtk.MessageDialog.__init__(self, parent, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.NONE, "Your Laptop's Resolution and Scaling Were Automatically Set.")
        self.set_markup("<span weight=\"bold\" size=\"larger\">Your Laptop's Resolution and Scaling Were Automatically Set</span>")
        nvidia_warning = """Please use the NVIDIA X Server Settings tool to arrange your displays.\n\n"""
        if model in INTEL:
            nvidia_warning = """"""
        secondary_markup = """This will allow normal use of the external display. Graphics on your laptop's display may appear less sharp while an external display is connected, and some apps may need to be restarted.\n\n""" + nvidia_warning + """For more information, see <a href=\"http://support.system76.com/articles/hidpi-multi-monitor/\">this System76 Support article</a>"""
        self.format_secondary_markup(secondary_markup)
        
        self.active = True
        
        self.add_buttons("Revert", Gtk.ResponseType.CANCEL)
        self.add_buttons("Keep Changes", Gtk.ResponseType.OK)
        action_area = self.get_action_area()
        action_area.set_layout (Gtk.ButtonBoxStyle.END)
        
        image = Gtk.Image()
        image.set_from_icon_name("preferences-desktop-display", Gtk.IconSize.DIALOG)
        image.show()
        self.set_image(image)
        
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(False)
        self.set_title("System76 HiDPI Scaling")
        self.set_icon_name("preferences-desktop-display")
        self.thread = None
        
    def on_checkbox_toggled(self, button):
        if button.get_active():
            self.active = False
        else:
            self.active = True
                
    def run(self, hotplug):
        time.sleep(2)
        self.thread = threading.Thread(target=hotplug.run)
        self.thread.start()
        return super(HotplugDialog, self).run()
        
    def destroy(self, hotplug):
        hotplug.transfer_timeout = True
        hotplug.active = self.active
        super(HotplugDialog, self).destroy()
        

class HotplugAutoscaling:
    def __init__(self, model):
        self.model = model
        self.xrandr = ""
        self.displays = dict() # {'LVDS-0': 'connected', 'HDMI-0': 'disconnected'}
        self.display_modes = [] # Keep track of each display's X attributes
        self.unityscales = {}
        self.dialog = None
        self.transfer_timeout = False
        self.panning_entries = []
        self.screen_maximum = XRes(x=0, y=0)
        self.active = True
        self.has_internal_hidpi = False
        self.update_rate = 2
        
    def find_internal_hidpi(self):
        for display in self.display_modes:
            xstr, ystr = self.get_display_dpi(display)
            if display.display in ['DP-0', 'eDP-1'] and (xstr > 170 or ystr > 170):
                self.has_internal_hidpi = True
    
    def set_update_rate(self):
        self.read_xrandr()
        self.update_display_modes()
        if self.has_internal_hidpi:
            self.update_rate = 2
            return
        self.update_rate = 200
    
    def detect_hotplug_changes(self):
        if True:
            reg = re.compile(r'^DP-0|eDP-1\b', re.MULTILINE)
            if not reg.findall(str(self.xrandr)):
                log.info('Could not find internal display in xrandr.')
                return False
            reg = re.compile(r'^((?:eDP|DP|HDMI|DVI|VGA|LVDS)-[0-9](?:.[0-9])?) (connected|disconnected)\b', re.MULTILINE)
            xrandr_tokens = reg.findall(str(self.xrandr))
            
            if self.displays == {}:
                self.displays = dict(xrandr_tokens)
                # Daemon has just started.  Check for external monitors that need setup.
                # Report a hotplug change if we find any.
                for display in self.displays:
                    status = self.displays[display]
                    if display not in ['DP-0', 'eDP-1'] and status == 'connected':
                        return True
                return False
                
            new_displays = dict(xrandr_tokens)
            for display in new_displays:
                status = new_displays[display]
                old_displays = self.displays
                if display in old_displays:
                    old_status = old_displays[display]
                    if status != old_status:
                        self.displays = new_displays
                        return True
                else:
                    self.displays = new_displays
                    return True
                    
            self.displays = new_displays
            return False 
            
        else:
            log.info("Couldn't detect hotplug changes")
    
    def compiz_workarounds(self):
        if self.model in INTEL:
            return
        gtk_theme = ""
        for value in ['true', 'false']:
            if value == 'false':
                time.sleep(1)
            cmd = ['gsettings', 'set', 'org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/', 'override-decoration-theme', value]
            SubProcess.check_output(cmd)
            
            if value == 'true':
                cmd = ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme']
                gtk_theme = SubProcess.check_output(cmd)
                cmd = ['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', '']
                SubProcess.check_output(cmd)
            else:
                cmd = ['gsettings', 'set', 'org.gnome.desktop.interface', 'gtk-theme', gtk_theme]
                SubProcess.check_output(cmd)
    
    def read_xrandr(self):
        cmd = ['xrandr']
        try:
            xrandr_output = SubProcess.check_output(cmd)
            xrandr_string = xrandr_output.decode("utf-8")
        except:
            log.info('failed to call xrandr: Is X running?')
            return False
        
        try:
            self.xrandr = xrandr_string
            
            reg = re.compile(r'Screen .*? maximum (\d+) x (\d+)')
            screen_tokens = reg.findall(str(xrandr_string))
            for (max_x, max_y) in screen_tokens:
                self.screen_maximum = XRes(x=int(max_x), y=int(max_y))
            
            # Check for internal display
            reg = re.compile(r'^DP-0|eDP-1\b', re.MULTILINE)
            if not reg.findall(str(xrandr_string)):
                log.info('Could not find internal display in xrandr.')
                return False
        except:
            return False
    
    def revert_display_settings(self):
        if self.dialog:
            self.dialog.destroy(self)
            self.dialog = None
        self.calculate_layout(revert=True)
        
        cmd = ['xrandr']
        for display in self.display_modes:
            mode = display.modes[0]
            pan_x, pan_y = self.get_display_panning(display)
            if self.model in NVIDIA:
                cmd = cmd + ['--output', display.display, 
                    '--scale', '1x1',
                    '--panning', str(mode.x) + 'x' + str(mode.y) + '+' + str(pan_x) + '+' + str(pan_y) 
                    + '/tracking:' + str(mode.x) + 'x' + str(mode.y) + '+0+0/border:0/0/0/0']
            if self.model in INTEL:
                cmd = cmd + ['--output', display.display, 
                    '--mode', str(mode.x) + 'x' + str(mode.y), 
                    '--pos', str(pan_x) + 'x' + str(pan_y)]
            
        try:
            SubProcess.check_output(cmd)
            cmd_gsettings = ['gsettings', 'reset', 'com.ubuntu.user-interface', 'scale-factor']
            SubProcess.check_output(cmd_gsettings)
            time.sleep(1)
            SubProcess.check_output(cmd_gsettings)
        except:
            log.info("Couldn't revert display settings.")
        #self.compiz_workarounds()
    
    def show_dialog(self):
        if not self.dialog:
            self.transfer_timeout = True
            self.dialog = HotplugDialog(Gtk.Window(), self.model)
            response = self.dialog.run(self)
            if response == Gtk.ResponseType.CANCEL:
                self.revert_display_settings()
            elif response == Gtk.ResponseType.OK:
                pass
            if self.dialog is not None:
                self.dialog.destroy(self)
                self.dialog = None
    
    def calculate_layout(self, revert=False):
        cur_pos_sorted_x = dict()
        cur_pos_sorted_y = dict()
        display_pannings = dict()
        
        # Organize displays by current horizontal and vertical position.
        for display in self.display_modes:
            if display.panning.pos_x in cur_pos_sorted_x:
                cur_pos_x_entries = cur_pos_sorted_x[display.panning.pos_x]
                cur_pos_x_entries.append(display.display)
            else:
                cur_pos_x_entries = [display.display]
            if display.panning.pos_y in cur_pos_sorted_y:
                cur_pos_y_entries = cur_pos_sorted_y[display.panning.pos_y]
                cur_pos_y_entries.append(display.display)
            else:
                cur_pos_y_entries = [display.display]
            cur_pos_sorted_x[display.panning.pos_x] = cur_pos_x_entries
            cur_pos_sorted_y[display.panning.pos_y] = cur_pos_y_entries
        
        prev_right = 0
        prev_top = 0
        prev_bottom = 0
        # Layout displays without overlap starting with top-left-most display,
        # working to the left and down.  We need to make sure not to exceed
        # the maximum X screen size.  Intel graphics are limited to 8192x8192, 
        # so a hidpi internal display and two external displays can exceed this
        # limit. 
        for y in sorted(cur_pos_sorted_y):
            for x in sorted(cur_pos_sorted_x):
                for display_name in cur_pos_sorted_x[x]:
                    if display_name in cur_pos_sorted_y[y]:
                        
                        display = None
                        for d in self.display_modes:
                            if d.display == display_name:
                                display = d
                        
                        xdpi, ydpi = self.get_display_dpi(display)
                        if (xdpi > 170 or ydpi > 170) and revert == False:
                            cur_factor = 2
                        else:
                            cur_factor = 1
                        x_log_res, y_log_res = self.get_display_logical_resolution(display, cur_factor)
                        
                        display_left = prev_right
                        display_top = prev_top
                        if display_left + x_log_res > self.screen_maximum.x:
                            display_left = 0
                            display_top = prev_bottom
                            if display_top + y_log_res > self.screen_maximum.y:
                                log.info("Too many displays to position within X screen boundaries.")
                                pass
                        
                        display_pannings[display_name] = (display_left, display_top)
                        
                        prev_right = display_left + x_log_res
                        prev_top = display_top
                        if prev_bottom < display_top + y_log_res:
                            prev_bottom = display_top + y_log_res
                            
        self.panning_entries = display_pannings
    
    def get_display_panning(self, display):
        (x, y) = self.panning_entries[display.display]
        return x, y
    
    def get_display_dpi(self, display):
        width, height = display.size
        mode = display.modes[0]
        x_res, y_res = mode
        
        # Some displays report aspect ratio instead of actual dimensions.
        if width == 160 and height == 90:
            if x_res >= 3840 and y_res >= 2160:
                return 192, 192
            else:
                return 96, 96
            
        if width > 0 and height > 0:
            dpi_x = x_res/width * 25.4
            dpi_y = y_res/height * 25.4
            return dpi_x, dpi_y
        else:
            return None, None
    
    def get_display_logical_resolution(self, display, scale_factor):
        x_res = display.modes[0].x
        y_res = display.modes[0].y
        return int(x_res/scale_factor), int(y_res/scale_factor)
    
    def set_display_scaling(self, display, force_lowdpi=False):
        xdpi, ydpi = self.get_display_dpi(display)
        
        if force_lowdpi == True:
                cmd_gs = ['gsettings', 'set', 'com.ubuntu.user-interface', 'scale-factor', str(self.unityscales)]
                try:
                    SubProcess.check_output(cmd_gs)
                except:
                    log.info("Failed to set Unity scaling factor.")
                
                pan_x, pan_y = self.get_display_panning(display)
                cmd = ['--output', display.display, 
                    '--scale', '1x1', 
                    '--panning', str(int(display.modes[0].x)) + 'x' + str(int(display.modes[0].y)) 
                        + '+' + str(pan_x) + '+' + str(pan_y)]
                if self.model in INTEL:
                    cmd = ['--output', display.display, 
                        '--mode', str(int(display.modes[0].x)) + 'x' + str(int(display.modes[0].y)), 
                        '--pos', str(pan_x) + 'x' + str(pan_y)]
                    
        if xdpi > 170 or ydpi > 170:
            if force_lowdpi == True:
                x,y = self.get_display_logical_resolution(display, 2)
                cmd = ['--output', display.display, 
                    '--scale', '0.5x0.5', 
                    '--panning', str(int(display.modes[0].x/2)) + 'x' + str(int(display.modes[0].y/2)) 
                        + '+' + str(pan_x) + '+' + str(pan_y)]
                if self.model in INTEL:
                    cmd = ['--output', display.display, 
                    '--mode', str(int(display.modes[0].x/2)) + 'x' + str(int(display.modes[0].y/2)), 
                    '--pos', str(pan_x) + 'x' + str(pan_y)]
        return cmd
    
    def update_display_modes(self):
        reg = re.compile(r'''^((?:eDP|DP|HDMI|DVI|VGA|LVDS)-[(0-9)](?:.[0-9])?) (connected|disconnected).*?(\d+)x(\d+)\+(\d+)\+(\d+).*?(\d+)mm\ x\ (\d+)mm|^   ([0-9]{3,4})x([0-9]{3,4})''', re.MULTILINE)
        xrandr_tokens = reg.findall(str(self.xrandr))
        
        display_list = []
        current_display = None
        current_mode_list = []
        for (display, status, pan_res_x, pan_res_y, pan_pos_x, pan_pos_y, width, height, x_res, y_res) in xrandr_tokens:
            if display != '' and status != '':
                # Beginning of new display.  The previous display is complete,
                # so let's append it to the list.
                if current_display is not None:
                    display_list.append(current_display)
                    current_mode_list = []
                
                # Then if we have physical display dimensions,
                # start building new display.
                if height.isdecimal() and width.isdecimal():
                    #we have physical display dimensions
                    #now setup new display
                    size_nt = XSize(width=int(width), height=int(height))
                    panning_nt = XPanning(res_x=pan_res_x, 
                                          res_y=pan_res_y, 
                                          pos_x=pan_pos_x, 
                                          pos_y=pan_pos_y)
                    current_display = XDisplay(display=display, 
                                                  size=size_nt, 
                                                  panning=panning_nt,
                                                  modes=[])
                else:
                    # Ignore this display.  
                    # It didn't report a physical size, so we can't determine it's density.
                    current_display = None
            else:
                # Make sure we actually have a current display.
                # Bug with simultaneous displays suddenly not reporting physical
                # dimensions makes this check necessary.
                if current_display == None:
                    log.info("Failed to generate XDisplay data: Is xrandr reporting physical size?")
                    self.read_xrandr()
                    time.sleep(1)
                    self.change_scaling_mode()
                    return
                if x_res.isdecimal() and y_res.isdecimal():
                    # Got mode line. Append it to the current display.
                    current_mode_list.append(XRes(x=int(x_res), y=int(y_res)))
                    current_display.modes.append(XRes(x=int(x_res), y=int(y_res)))
        
        current_display.modes.append(current_mode_list)
        display_list.append(current_display)
        self.display_modes = display_list
        
        self.find_internal_hidpi()
    
    def change_scaling_mode(self):
        try:
            self.update_display_modes()
            self.calculate_layout()
        except:
            log.exception("Couldn't update display modes")
        
        # Don't manage display modes on non-hidpi laptops.  However, once we start
        # managing displays we need to keep doing so.
        if not self.has_internal_hidpi:
            return False
            
        internal_hidpi = False
        external_lowdpi = False
        # Check for low-dpi displays
        for display in self.display_modes:
            xstr, ystr = self.get_display_dpi(display)
            if display.display in ['DP-0', 'eDP-1'] and (xstr > 170 or ystr > 170):
                internal_hidpi = True
            elif xstr == None or ystr == None:
                pass
            elif xstr > 170 or ystr > 170:
                pass
            else:
                external_lowdpi = True
            
        if internal_hidpi == True and external_lowdpi == True:
            # Assemble xrandr command to set scaling for all displays
            cmd_list = ['xrandr']
            for display in self.display_modes:
                self.unityscales[display.display] = 8
                cmd_part = self.set_display_scaling(display, force_lowdpi=True)
                if cmd_part != None:
                    for part in cmd_part:
                        cmd_list.append(part)
            # Set xrandr display configuration.  
            # If using NVIDIA graphics, reconfigure X Screen size to avoid problems.
            SubProcess.check_output(cmd_list)
            
            if self.model not in INTEL:
                cmd = ['xrandr', '-s', '0']
                SubProcess.check_output(cmd)
                # The NVIDIA driver 375.39 causes corruption on Compiz when changing xrandr config.  
                # The theme will flicker for a moment.
                # FIXED in NVIDIA driver 375.66
                #self.compiz_workarounds()
            
            self.show_dialog()
        else:
            if internal_hidpi == True and external_lowdpi == False:
                for display in self.display_modes:
                    self.unityscales[display.display] = 16
            self.revert_display_settings()
        
        return True;
    
    def run(self):
        self.set_update_rate()
        self.transfer_timeout = False
        self.timeout_id = GLib.timeout_add(self.update_rate * 1000, self.on_timeout)
        
    def on_timeout(self):
        try:
            self.update()
            if self.transfer_timeout:
                self.transfer_timeout = False
                return False
            return True
        except Exception:
            log.exception('Error calling HotplugAutoscaling.update():')
            return False
    
    def update(self):
        if not self.active:
            self.transfer_timeout = True
            return
        self.read_xrandr()
        changed = self.detect_hotplug_changes()
        if changed:
            try:
                self.change_scaling_mode()
            except:
                log.exception('Error changing display scaling mode, reverting.')
                self.revert_display_settings()
        else:
            return

def _run_hotplug_autoscaling(model):
    if model not in NEEDS_HOTPLUG_AUTOSCALING:
        log.info('Hotplug Autoscaling not needed for %r', model)
        return
    log.info('Hotplug autoscaling for %r', model)
    
    if model in MODEL_MODES:
        try:
            # Using subprocess.call() with shell=True because of way xrandr 
            # --newmode needs its arguments.  A better method would be nice.
            cmd = 'xrandr' + ' --newmode ' + MODEL_MODES[model]
            subprocess.call(cmd, shell=True)
        except:
            log.info('Failed to create new xrandr mode. It may exist already.')
        try:
            cmd = ['xrandr', '--addmode'] + ['eDP-1', '1600x900']
            SubProcess.check_output(cmd)
        except:
            log.warning("Failed to add xrandr mode to display.")
    
    hotplug = HotplugAutoscaling(model)
    hotplug.run()
    mainloop = GLib.MainLoop()
    mainloop.run()
    
    return hotplug
    
def run_hotplug_autoscaling(model):
    try:
        return _run_hotplug_autoscaling(model)
    except Exception:
        log.exception('Error calling _run_hotplug_autoscaling(%r):', model)
