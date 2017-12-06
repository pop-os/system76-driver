from Xlib import X
from Xlib import display as xdisplay
from Xlib.ext import randr
from Xlib.protocol import rq
import logging
import time

import subprocess
import re
import threading, queue
from shutil import which
from collections import namedtuple

from system76driver import dbusutil

log = logging.getLogger(__name__)

NEEDS_HIDPI_AUTOSCALING = (
    'bonw12',
    'galp2',
    'galp3',
    'oryp2-ess',
    'oryp3-ess',
    'oryp3',
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
    'galp3',
}

MODEL_MODES = {
    'galp2': '1600x900  118.25  1600 1696 1856 2112  900 903 908 934 -hsync +vsync',
    'galp3': '1600x900  118.25  1600 1696 1856 2112  900 903 908 934 -hsync +vsync',
}

#            name       pclk   hdisp,hsyncstart,hsyncend,hsyncend,htotal, v..., flags
#            '1600x900  118.25  1600 1696 1856 2112  900 903 908 934 -hsync +vsync',


# INCLUDING Patched python-xlib code (upstream since 2011), since the Ubuntu packages are even older.
# the patched code fixes a bug where part/all of the display name is missing when a display is plugged in.
extname = 'RANDR'

class DPIGetOutputInfo(rq.ReplyRequest):
    _request = rq.Struct(
        rq.Card8('opcode'),
        rq.Opcode(9),
        rq.RequestLength(),
        rq.Card32('output'),
        rq.Card32('config_timestamp'),
        )
    _reply = rq.Struct(
        rq.ReplyCode(),
        rq.Card8('status'),
        rq.Card16('sequence_number'),
        rq.ReplyLength(),
        rq.Card32('timestamp'),
        rq.Card32('crtc'),
        rq.Card32('mm_width'),
        rq.Card32('mm_height'),
        rq.Card8('connection'),
        rq.Card8('subpixel_order'),
        rq.LengthOf('crtcs', 2),
        rq.LengthOf('modes', 2),
        rq.Card16('num_preferred'),
        rq.LengthOf('clones', 2),
        rq.LengthOf('name', 2),
        rq.List('crtcs', rq.Card32Obj),
        rq.List('modes', rq.Card32Obj),
        rq.List('clones', rq.Card32Obj),
        rq.String8('name'),
)

def dpi_get_output_info(d, output, config_timestamp):
    return DPIGetOutputInfo(
        display=d.display,
        opcode=d.display.get_extension_major(extname),
        output=output,
        config_timestamp=config_timestamp,
)


class DPIGetCrtcInfo(rq.ReplyRequest):
    _request = rq.Struct(
        rq.Card8('opcode'),
        rq.Opcode(20),
        rq.RequestLength(),
        rq.Card32('crtc'),
        rq.Card32('config_timestamp'),
        )
    _reply = rq.Struct(
        rq.ReplyCode(),
        rq.Card8('status'),
        rq.Card16('sequence_number'),
        rq.ReplyLength(),
        rq.Card32('timestamp'),
        rq.Int16('x'),
        rq.Int16('y'),
        rq.Card16('width'),
        rq.Card16('height'),
        rq.Card32('mode'),
        rq.Card16('rotation'),
        rq.Card16('possible_rotations'),
        rq.LengthOf('outputs', 2),
        rq.LengthOf('possible_outputs', 2),
        rq.List('outputs', rq.Card32Obj),
        rq.List('possible_outputs', rq.Card32Obj),
        )

def dpi_get_crtc_info(d, crtc, config_timestamp):
    return DPIGetCrtcInfo (
        display=d.display,
        opcode=d.display.get_extension_major(extname),
        crtc=crtc,
        config_timestamp=config_timestamp,
)


class DPICreateMode(rq.ReplyRequest):
    _request = rq.Struct(
        rq.Card8('opcode'),
        rq.Opcode(16),
        rq.RequestLength(),
        rq.Window('window'),
        rq.Object('mode', randr.RandR_ModeInfo),
        rq.String8('name'),
        )
    _reply = rq.Struct(
        rq.ReplyCode(),
        rq.Pad(1),
        rq.Card16('sequence_number'),
        rq.ReplyLength(),
        rq.Card32('mode'),
        rq.Pad(20),
        )

def dpi_create_mode(w, mode, name):
    return DPICreateMode (
        display=w.display,
        opcode=w.display.get_extension_major(extname),
        window=w,
        mode=mode,
        name=name,
)


class DPIAddOutputMode(rq.Request):
    _request = rq.Struct(
        rq.Card8('opcode'),
        rq.Opcode(18),
        rq.RequestLength(),
        rq.Card32('output'),
        rq.Card32('mode'),
        )

def dpi_add_output_mode(d, output, mode):
    return DPIAddOutputMode(
        display=d.display,
        opcode=d.display.get_extension_major(extname),
        output=output,
        mode=mode,
)


class DPISetCrtcConfig(rq.ReplyRequest):
    _request = rq.Struct(
        rq.Card8('opcode'),
        rq.Opcode(21),
        rq.RequestLength(),
        rq.Card32('crtc'),
        rq.Card32('timestamp'),
        rq.Card32('config_timestamp'),
        rq.Int16('x'),
        rq.Int16('y'),
        rq.Card32('mode'),
        rq.Card16('rotation'),
        rq.Pad(2),
        rq.List('outputs', rq.Card32Obj),
        )
    _reply = rq.Struct(
        rq.ReplyCode(),
        rq.Card8('status'),
        rq.Card16('sequence_number'),
        rq.ReplyLength(),
        rq.Card32('new_timestamp'),
        rq.Pad(20),
        )

def dpi_set_crtc_config(d, crtc, config_timestamp, x, y, mode, rotation, outputs, timestamp=X.CurrentTime):
    return DPISetCrtcConfig (
        display=d.display,
        opcode=d.display.get_extension_major(extname),
        crtc=crtc,
        config_timestamp=config_timestamp,
        x=x,
        y=y,
        mode=mode,
        rotation=rotation,
        outputs=outputs,
        timestamp=timestamp,
)

class DPIGetOutputProperty(rq.ReplyRequest):
    _request = rq.Struct(
        rq.Card8('opcode'),
        rq.Opcode(15),
        rq.RequestLength(),
        rq.Card32('output'),
        rq.Card32('property'),
        rq.Card32('type'),
        rq.Card32('long_offset'),
        rq.Card32('long_length'),
        rq.Bool('delete'),
        rq.Bool('pending'),
        rq.Pad(2),
        )
    _reply = rq.Struct(
        rq.ReplyCode(),
        rq.Format('value', 1),
        rq.Card16('sequence_number'),
        rq.ReplyLength(),
        rq.Card32('property_type'),
        rq.Card32('bytes_after'),
        rq.LengthOf('value', 4),
        rq.Pad(12),
        rq.List('value', rq.Card8Obj),
        )

def dpi_get_output_property(d, output, property, type, long_offset, long_length, delete=False, pending=False):
    return DPIGetOutputProperty(
        display=d.display,
        opcode=d.display.get_extension_major(extname),
        output=output,
        property=property,
        type=type,
        long_offset=long_offset,
        long_length=long_length,
        delete=delete,
        pending=pending,
)


XRes = namedtuple('XRes', ['x', 'y'])


class HiDPIAutoscaling:
    def __init__(self, model):
        self.model = model
        self.displays = dict() # {'LVDS-0': 'connected', 'HDMI-0': 'disconnected'}
        self.screen_maximum = XRes(x=8192, y=8192)
        self.pixel_doubling = False 
        self.scale_mode = 'lowdpi' # If we have nvidia with the proprietary driver, set to hidpi for pixel doubling
        self.notification = None
        self.queue = queue.Queue()
        self.unforce = False
        self.calculated_display_size = (0,0) # Used to hack around intel black band bug (wrong XScreen size)
        
        self.init_xlib()
        
    def init_xlib(self):
        self.xlib_display = xdisplay.Display()
        screen = self.xlib_display.screen()
        self.xlib_window = screen.root.create_window(10,10,10,10,0, 0, window_class=X.InputOnly, visual=X.CopyFromParent, event_mask=0)
        self.xlib_window.xrandr_select_input(randr.RRScreenChangeNotifyMask)
        #            | randr.RROutputChangeNotifyMask
        #            | randr.RROutputPropertyNotifyMask)
                    
        self.update_display_connections()
        if self.get_gpu_vendor() == 'nvidia':
            self.scale_mode = 'hidpi'
            self.screen_maximum = XRes(x=32768, y=32768)
        else:
            self.add_output_mode()

    #Test for nvidia proprietary driver and nvidia-settings
    def get_gpu_vendor(self):
        if self.model in INTEL:
            return 'intel'
        if which('nvidia-settings') is not None:
            return 'nvidia'
        else:
            return 'intel'
    
    def add_output_mode(self):
        # GALP2 EXAMPLE
        # name       pclk   hdisp,hsyncstart,hsyncend,hsyncend,htotal, v..., flags
        # '1600x900  118.25  1600 1696 1856 2112  900 903 908 934 -hsync +vsync',
        if self.model not in MODEL_MODES:
            return
        modeline = MODEL_MODES[self.model].split()
        mode_id = 0
        #mode_name = modeline[0]
        mode_clk = int(round(float(modeline[1])))
        mode_horizontal = [int(modeline[2]), int(modeline[3]), int(modeline[4]), int(modeline[5])]
        mode_vertical = [int(modeline[6]), int(modeline[7]), int(modeline[8])]
        mode_name_length = len(modeline[0])
        #flags = modeline[10:]
        mode_flags = int(randr.HSyncNegative | randr.VSyncPositive)
        newmode = (mode_id, 1600, 900, mode_clk) +  tuple(mode_horizontal) + tuple(mode_vertical) + ( mode_name_length, mode_flags )
        try:
            dpi_create_mode(self.xlib_window, newmode, '1600x900')
        except:
            # We got an error, but it's fine.
            # Eventually, we'll need to handle picking a 'close' mode if we can't make one.
            pass
        
        time.sleep(0.1)
        resources = self.xlib_window.xrandr_get_screen_resources()._data
        selected_output = None
        for output in resources['outputs']:
            info = dpi_get_output_info(self.xlib_display, output, resources['config_timestamp'])._data
            if info['name'] == 'eDP-1':
                selected_output = output
        for mode in resources['modes']:
            if mode['width'] == 1600 and mode['height'] == 900:
                dpi_add_output_mode(self.xlib_display, selected_output, mode['id'])
    
    def update_display_connections(self):
        resources = self.xlib_window.xrandr_get_screen_resources()._data
        
        modes = dict()
        for mode in resources['modes']:
            modes[mode['id']] = mode
        
        new_displays = dict()
        for output in resources['outputs']:
            info = dpi_get_output_info(self.xlib_display, output, resources['config_timestamp'])._data
            modelist = []
            for mode_id in info['modes']:
                mode = modes[mode_id]
                modelist.append(mode._data)
            new_displays[info['name']] = dict()
            new_displays[info['name']]['connected'] = not bool(info['connection'])
            new_displays[info['name']]['mm_width'] = info['mm_width']
            new_displays[info['name']]['mm_height'] = info['mm_height']
            new_displays[info['name']]['modes'] = modelist
            new_displays[info['name']]['crtc'] = info['crtc']
            
            # Get connector type for each display. 'Panel' indicates internal display.
            new_displays[info['name']]['connector_type'] = ''
            properties_list = self.xlib_display.xrandr_list_output_properties(output)._data
            for atom in properties_list['atoms']:
                atom_name = self.xlib_display.get_atom_name(atom)
                if atom_name == randr.PROPERTY_CONNECTOR_TYPE:
                    prop = dpi_get_output_property(self.xlib_display, output, atom, 4, 0, 100)._data
                    connector_type = self.xlib_display.get_atom_name(prop['value'][0])
                    new_displays[info['name']]['connector_type'] = connector_type
        
        for display in new_displays:
            status = new_displays[display]['connected']
            if display in self.displays:
                old_status = self.displays[display]['connected']
                if status != old_status:
                    self.displays = new_displays
                    return True
                # Need to check for laptop lid closed.
                # When laptop lid is closed, crtc is 0, when open it should be a positive integer.
                new_crtc = new_displays[display]['crtc']
                old_crtc = self.displays[display]['crtc']
                if new_crtc != old_crtc:
                    if new_crtc == 0 or old_crtc == 0:
                        self.displays = new_displays
                        return True
            else:
                self.displays = new_displays
                return True
        
        self.displays = new_displays
        return False
    
    def notification_update(self, has_mixed_dpi, unforce):
        if not has_mixed_dpi:
            self.notification.terminate()
        else:
            self.notification.terminate()
            # uncomment if disabling persistent notifications
            #self.send_scaling_notification( queue=self.queue, unforce=unforce)
    
    def notification_return(self):
        if self.notification.returncode == 76:
            if self.queue is not None:
                if self.get_gpu_vendor() == 'nvidia':
                    if self.scale_mode == 'hidpi':
                        self.scale_mode = 'lowdpi'
                    else:
                        self.scale_mode = 'hidpi'
                else:
                    self.unforce = not self.unforce
                self.queue.put(self.scale_mode)
                self.queue.put(self.unforce)
            if self.get_gpu_vendor() == 'intel':
                # for threading reasons, create a new autoscaling instance...but do not call run() on it!
                h = HiDPIAutoscaling(self.model)
                h.unforce = self.unforce
                h.set_scaled_display_modes(notification=False)
                self.send_scaling_notification(self.queue, unforce=self.unforce)
            if self.get_gpu_vendor() == 'nvidia': # nvidia
                h = HiDPIAutoscaling(self.model)
                h.scale_mode = self.scale_mode
                h.set_scaled_display_modes(notification=False)
                self.send_scaling_notification(self.queue)
        else:
            self.send_scaling_notification(self.queue, unforce=self.unforce)
    
    def send_scaling_notification(self, queue=None, unforce=False):
        if self.unforce:
            scale_mode="unforce"
        else:
            scale_mode=self.scale_mode
        
        # Change notification text on intel graphics if we only have hidpi displays
        gpu_vendor = self.get_gpu_vendor()
        if gpu_vendor == 'intel':
            has_mixed_dpi, has_hidpi, has_lowdpi = self.has_mixed_hi_low_dpi_displays()
            if has_hidpi and not has_mixed_dpi:
                gpu_vendor = 'nvidia'
                if scale_mode == "unforce":
                    scale_mode='hidpi'
        def cmd_in_thread(on_done, cmd):
            self.notification = subprocess.Popen(cmd)
            if queue is not None:
                queue.put(self.notification)
            self.notification.wait()
            on_done()
            
        cmd = ['/usr/lib/system76-driver/system76-hidpi-notification', '--scale-mode=' + scale_mode, '--gpu-vendor=' + gpu_vendor]
        thread = threading.Thread(target=cmd_in_thread, args=(self.notification_return, cmd))
        thread.daemon = True
        thread.start()
        
        return False        
        
    def get_display_position(self, display_name):
        resources = self.xlib_window.xrandr_get_screen_resources()._data
        crtc = self.displays[display_name]['crtc']
        connected = self.displays[display_name]['connected']
        if crtc != 0:
            crtc_info = dpi_get_crtc_info(self.xlib_display, crtc, resources['config_timestamp'])._data
            return crtc_info['x'], crtc_info['y']
        elif connected == True and not self.panel_activation_override(display_name):
            return 0, 0
        else:
            return -1, -1
    
    def get_display_dpi(self, display_name):
        width = self.displays[display_name]['mm_width']
        height = self.displays[display_name]['mm_height']
        try:
            mode = self.displays[display_name]['modes'][0]
        except:
            return None
        x_res = mode['width']
        y_res = mode['height']
        
        # Some displays report aspect ratio instead of actual dimensions.
        if width == 160 and height == 90:
            if x_res >= 3840 and y_res >= 2160:
                return 192, 192
            else:
                return 96, 96
        
        if width > 0 and height > 0:
            dpi_x = x_res/width * 25.4
            dpi_y = y_res/height * 25.4
            return max(dpi_x, dpi_y)
        elif width == 0 and height == 0:
            return 0
        else:
            return None
        
    def get_display_logical_resolution(self, display_name, scale_factor):
        try:
            mode = self.displays[display_name]['modes'][0]
            x_res = mode['width']
            y_res = mode['height']
            return int(x_res/scale_factor), int(y_res/scale_factor)
        except:
            return 0, 0
    
    def calculate_layout(self, revert=False):
        position_lookup_entries_x = dict()
        position_lookup_entries_y = dict()
        cur_position_entries_x = list()
        cur_position_entries_y = list()
        
        display_positions = dict()
        
        for display in self.displays:
            position_x, position_y = self.get_display_position(display)
            if position_x != -1 and position_y != -1:
                if position_x in position_lookup_entries_x:
                    cur_position_entries_x = position_lookup_entries_x[position_x]
                    cur_position_entries_x.append(display)
                else:
                    cur_position_entries_x = [display]
                if position_y in position_lookup_entries_y:
                    cur_position_entries_y = position_lookup_entries_y[position_y]
                    cur_position_entries_y.append(display)
                else:
                    cur_position_entries_y = [display]
                position_lookup_entries_x[position_x] = cur_position_entries_x
                position_lookup_entries_y[position_y] = cur_position_entries_y
        
        prev_right = 0
        prev_top = 0
        prev_bottom = 0
        # Layout displays without overlap starting with top-left-most display,
        # working to the left and down.  We need to make sure not to exceed
        # the maximum X screen size.  Intel graphics are limited to 8192x8192,
        # so a hidpi internal display and two external displays can exceed this
        # limit.
        for y in sorted(position_lookup_entries_y):
            for x in sorted(position_lookup_entries_x):
                for display_name in position_lookup_entries_x[x]:
                    if display_name in position_lookup_entries_y[y]:
                        display = None
                        for d in self.displays:
                            if d == display_name:
                                display = d
                                
                        dpi = self.get_display_dpi(display)
                        if dpi is None:
                            scale_factor = 1
                        elif dpi > 170 and revert == False:
                            scale_factor = 2
                        else:
                            scale_factor = 1
                            
                        if self.scale_mode == 'hidpi' and revert == False:
                            scale_factor = scale_factor / 2
                            
                        logical_resolution_x, logical_resolution_y = self.get_display_logical_resolution(display, scale_factor)
                        
                        display_left = prev_right
                        display_top = prev_top
                        if display_left + logical_resolution_x > self.screen_maximum.x:
                            display_left = 0
                            display_top = prev_bottom
                            if display_top + logical_resolution_y > self.screen_maximum.y:
                                log.info("Too many displays to position within X screen boundaries.")
                                pass
                        
                        display_positions[display_name] = (display_left, display_top)
                        
                        prev_right = display_left + logical_resolution_x
                        prev_top = display_top
                        if prev_bottom < display_top + logical_resolution_y:
                            prev_bottom = display_top + logical_resolution_y
        
        # Work around Mutter(?) bug where the X Screen (not output) resolution is set too small.
        if self.get_gpu_vendor() == 'intel':
            self.calculated_display_size = (prev_right, prev_bottom)
        
        return display_positions

    def get_internal_lid_state(self):
        try:
            lid_file = open('/proc/acpi/button/lid/LID0/state', 'r')
            if 'open' in lid_file.read():
                return True
            else:
                return False
        except:
            log.info('Could not find lid state.  System may not be a laptop.')
            return True
    
    def panel_activation_override(self, display_name):
        try:
            if 'eDP' in display_name or self.displays[display_name]['connector_type'] == 'Panel':
                if not self.get_internal_lid_state():
                    #Don't activate display
                    return True
        except:
            return False
        return False
    
    def get_nvidia_settings_options(self, display_name, viewportin, viewportout):
        cmd = [ 'nvidia-settings', '-q', 'CurrentMetaMode' ]
        output = subprocess.check_output(cmd).decode("utf-8")
        deprettified_currentmetamode = re.sub(r'(\n )|(\n\n)', r'', output)
        
        dpys = subprocess.check_output(['nvidia-settings', '-q', 'dpys'])
        reg = re.compile(r'\[([0-9])\] (?:.*?)\[dpy\:([.0-9])\] \((.*?)\)')
        tokens = reg.findall(str(dpys))
        dpy_mapping = {}
        for entry in tokens:
            idx, dpy_num, connector_name = entry
            dpy_mapping["DPY-" + dpy_num] = connector_name

        reg = re.compile(r'((?:DPY\-\d).*?})')
        reg = re.compile(r'(DPY\-\d).*?(\{.*?\})')
        display_attribute_pairs = reg.findall(deprettified_currentmetamode)
        attribute_mapping = {}
        for pair in display_attribute_pairs:
            connector_name = dpy_mapping[pair[0]]
            if connector_name == display_name:
                attributes = pair[1]
                attributes = re.sub(r'ViewPortIn\=\d*x\d*(, )?', r'', attributes)
                attributes = re.sub(r'ViewPortOut\=\d*x\d*\+\d\+\d(, )?', r'', attributes)
                attributes = re.sub(r'ForceCompositionPipeline=\w*(, )?', r'', attributes)
                attributes = re.sub(r'{', r'{ViewPortOut=' + viewportout + ', ', attributes)
                attributes = re.sub(r'{', r'{ViewPortIn=' + viewportin + ', ', attributes)
                attributes = re.sub(r'}', r'ForceCompositionPipeline=On}, ', attributes)
                attribute_mapping[connector_name] = attributes
        
        # Create new attributes if we are activating a currently inactive display.
        # This fixes issues when plugging multiple displays in at the same time.
        if display_name not in attribute_mapping:
            attributes = '{ViewPortIn=' + viewportin + ', ' + \
                        'ViewPortOut=' + viewportout + ', ' + \
                        'ForceCompositionPipeline=On},'
            attribute_mapping[display_name] = attributes
        
        return attribute_mapping[display_name]


    def set_display_scaling_nvidia_settings(self, display_name, layout):
        #DP-0: nvidia-auto-select @3840x2160 +0+0 {ViewPortIn=3840x2160, ViewPortOut=3840x2160+0+0, ForceCompositionPipeline=On}
        #DISPLAY_NAME
        #nvidia-auto-select
        #@panning res
        #+pan_x+pan_y
        #{ViewPortIn=,ViewPortOut=
        #other attributes from matched display
        #ForceCompositionPipeline=On}
        
        # Don't generate config for laptop display if the lid is closed.
        if self.panel_activation_override(display_name):
            return ''
        
        dpi = self.get_display_dpi(display_name)
        if dpi is None:
            return ''
        display_str = display_name + ": nvidia-auto-select "
        
        mode = self.displays[display_name]['modes'][0]
        res_out_x = mode['width']
        res_out_y = mode['height']
        
        if self.scale_mode == 'hidpi':
            if dpi > 170:
                res_in_x = mode['width']
                res_in_y = mode['height']
            else:
                res_in_x = 2 * mode['width']
                res_in_y = 2 * mode['height']
        else:
            if dpi > 170:
                res_in_x = round(mode['width'] / 2)
                res_in_y = round(mode['height'] / 2)
            else:
                res_in_x = mode['width']
                res_in_y = mode['height']
        
        if display_name in layout:
            pan_x, pan_y = layout[display_name]
        else:
            return ''
        panning_pos = "+" + str(pan_x) + "+" + str(pan_y)
        
        viewportin = str(res_in_x) + "x" + str(res_in_y) + " "
        viewportout = str(res_out_x) + "x" + str(res_out_y) + panning_pos
        
        display_str = display_str + "@" + str(res_in_x) + "x" + str(res_in_y) + " "
        display_str = display_str + "+" + str(pan_x) + "+" + str(pan_y) + " "
        display_str = display_str + self.get_nvidia_settings_options(display_name, viewportin, viewportout)
        return display_str
        
    def set_display_scaling_xrandr(self, display_name, layout, force_lowdpi=True):
        dpi = self.get_display_dpi(display_name)
        
        resources = self.xlib_window.xrandr_get_screen_resources()._data
        
        if dpi is None:
            return ''
        mode = self.displays[display_name]['modes'][0]
        crtc = self.displays[display_name]['crtc']
        
        try:
            crtc_info = dpi_get_crtc_info(self.xlib_display, crtc, resources['config_timestamp'])._data
        except:
            return ''
        if force_lowdpi == True and dpi > 170:
            x_res = round(mode['width'] / 2)
            y_res = round(mode['height'] / 2)
        else:
            x_res = mode['width']
            y_res = mode['height']
            
        if display_name in layout:
            pan_x, pan_y = layout[display_name]
        else:
            return ''
        
        #now find the mode we want
        new_mode = None
        for mode in self.displays[display_name]['modes']:
            if mode['width'] == x_res and mode['height'] == y_res:
                new_mode = mode
                break
        
        try:
            dpi_set_crtc_config(self.xlib_display,crtc, int(time.time()), int(pan_x), int(pan_y), new_mode['id'], crtc_info['rotation'], crtc_info['outputs'])
        except:
            log.info("Could not set CRTC for " + str(display_name))
        
        return ''
    
    def set_display_scaling(self, display, layout, force=False):
        if self.displays[display]['modes'] == []:
            return ''
        if self.get_gpu_vendor() == 'nvidia':
            return self.set_display_scaling_nvidia_settings(display, layout)
        elif self.get_gpu_vendor() == 'intel':
            return self.set_display_scaling_xrandr(display, layout, force_lowdpi=force)
    
    def has_mixed_hi_low_dpi_displays(self):
        found_hidpi = False
        found_lowdpi = False
        has_mixed_dpi = False
        for display in self.displays:
            if self.displays[display]['connected'] == True:
                dpi = self.get_display_dpi(display)
                if dpi > 170:
                    found_hidpi = True
                elif dpi == None:
                    pass
                elif self.panel_activation_override(display):
                    pass
                else:
                    found_lowdpi = True
        
        if found_hidpi == True and found_lowdpi == True:
            has_mixed_dpi = True
        
        return has_mixed_dpi, found_hidpi, found_lowdpi
    
    def set_scaled_display_modes(self, notification=True):
        layout = self.calculate_layout(revert=self.unforce)
        
        has_mixed_dpi, has_hidpi, has_lowdpi = self.has_mixed_hi_low_dpi_displays()
        
        # INTEL: match display scales unless user selects 'native resolution'
        if not self.unforce:
            force = has_hidpi
        else:
            force = False
        
        # For each connected display, configure display modes.
        cmd = ''
        for display in self.displays:
            if self.displays[display]['connected'] == True:
                # INTEL: set the display crtc
                # NVIDIA: just get display parameters for nvidia-settings line
                cmd = cmd + self.set_display_scaling(display, layout, force=force)
        # NVIDIA: got parameters for nvidia-settings - actually set display modes
        if self.get_gpu_vendor() == 'nvidia':
            if has_hidpi:
                # First set scale mode manually since Mutter can't see the effective display resolution.
                # Step 1) Let's try setting scale.  If this works, we can skip the later steps (less flickering).
                # Step 2) That didn't work.  We'll need to set everything up at the native resolution for Mutter 
                #         to accept the display configuration.  Calculate a layout and nvidia-settings cmd at 
                #         native resolution and set it momentarily.
                # Step 3) Try setting the scale with displays at native resolution.  This should almost always work.
                if self.scale_mode == 'lowdpi':
                    try:
                        dbusutil.set_scale(1)
                    except:
                        # Need to setup displays at native resolution before setting scale.
                        layout_native = self.calculate_layout(revert=True)
                        cmd_native = ''
                        for display in self.displays:
                            if self.displays[display]['connected'] == True:
                                cmd_native = cmd_native + self.set_display_scaling(display, layout_native, force=force)
                        subprocess.call('nvidia-settings --assign CurrentMetaMode="' + cmd_native + '"', shell=True)
                        try:
                            dbusutil.set_scale(1)
                        except:
                            log.info("Could not set Mutter scale mode lowdpi")
                elif dbusutil.get_scale() < 2.0:
                    #Need to set a display mode Mutter is happy with before setting scale
                    try:
                        dbusutil.set_scale(2)
                    except:
                        # Need to setup displays at native resolution before setting scale.
                        layout_native = self.calculate_layout(revert=True)
                        cmd_native = ''
                        for display in self.displays:
                            if self.displays[display]['connected'] == True:
                                cmd_native = cmd_native + self.set_display_scaling(display, layout_native, force=force)
                        subprocess.call('nvidia-settings --assign CurrentMetaMode="' + cmd_native + '"', shell=True)
                        try:
                            dbusutil.set_scale(2)
                        except:
                            log.info("Could not set Mutter scale mode hidpi")
                # Let things settle down.
                time.sleep(0.1)
                # Now call nvidia settings with the metamodes we calculated in set_display_scaling()
                subprocess.call('nvidia-settings --assign CurrentMetaMode="' + cmd + '"', shell=True)
                if self.scale_mode == 'lowdpi' and dbusutil.get_scale() > 1.0:
                    try:
                        dbusutil.set_scale(1)
                    except:
                        log.info("Could not set Mutter scale mode lowdpi")
            # We don't have any hidpi displays (maybe one was disconnected).
            # No need to call nvidia-settings, but the scale could still be 2x.
            # Set scale back to 1x, so the user isn't stuck with everything unusably large.
            elif has_lowdpi and dbusutil.get_scale() > 1:
                try:
                    dbusutil.set_scale(1)
                except:
                    log.info("Could not set Mutter scale mode only lowdpi")
        # Special cases on INTEL.  Specifically 'native resolution' mode has some quirks.
        elif self.get_gpu_vendor() == 'intel' and force == False:
            if dbusutil.get_scale() < 2:
                for display in self.displays:
                    if self.displays[display]['connected']:
                        # Under some circumstances, Mutter may not set the scaling.
                        # In 'native resolution' ('unforced') mode, we must set scaling if:
                        # a) - the internal panel is hidpi
                        # b) - there is an external panel between 170 and 192 dpi (mutter already sets scale if above 192)
                        #    - and no lowdpi monitors are present (1x scaling is better if there are)
                        if 'eDP' in display or self.displays[display]['connector_type'] == 'Panel':
                            if self.get_display_dpi(display) > 192:
                                try:
                                    dbusutil.set_scale(2)
                                except:
                                    log.info("Could not set Mutter scale internal hidpi")
                        elif self.get_display_dpi(display) > 170 and not has_lowdpi: # same thing for external displays
                            try:
                                dbusutil.set_scale(2)
                            except:
                                log.info("Could not set Mutter scale external hidpi")
        
        # Work around Mutter(?) bug where the X Screen (not output) resolution is set too small.
        # Because of this, sometimes some displays may be rendered partially or completely black.
        # Calling 'xrandr --auto' causes the correct screen size to be set without other notable changes.
        if self.get_gpu_vendor() == 'intel':
            size_x, size_y = self.calculated_display_size
            size_str = 'current ' + str(size_x) + ' x ' + str(size_y)
            xrandr_output = subprocess.check_output(['xrandr']).decode('utf-8')
            if size_str not in xrandr_output:
                if self.get_internal_lid_state():
                    subprocess.call('xrandr --auto', shell=True)
                    if force == False and dbusutil.get_scale() < 2:
                        try:
                            dbusutil.set_scale(2)
                        except:
                            log.info("Could not set Mutter scale for workaround.")
                else:
                    subprocess.call('xrandr --output eDP-1 --off', shell=True)
        
        # Displays are all setup - Notify the user!
        # Note: The notification creates a new HiDPIAutoscaling object and calls set_scaled_display_modes() on completion.
        #       The 'notification' argument prevents these non-running instances from creating extra dead, useless notifications.
        #       To ensure the displayed notification can interact with the instance in the main thread and avoid duplicates, 
        #       don't process notifications from this child if notification == False.
        # Otherwise, there are two cases...
        # a) Notification already exists:
        #    - we either need to update its contents (hidpi/mixed) or remove it (lowdpi-only)
        # b) Notification doesn't exist yet:
        #    - send a new notification
        # The notification is sent/resent in a separate thread since the main thread will block until the next xlib display event.
        self.prev_display_types = (has_mixed_dpi, has_hidpi, has_lowdpi)
        if self.notification and notification:
            thread = threading.Thread(target = self.notification_update, args=(has_hidpi, self.unforce), daemon=True)
            thread.start()
        elif has_hidpi and notification:
            thread = threading.Thread(target = self.send_scaling_notification, args=(self.queue, self.unforce), daemon=True)
            thread.start()
    
    def update(self, e):
        time.sleep(.1)
        if self.update_display_connections():
            has_mixed_dpi, has_hidpi, has_lowdpi = self.has_mixed_hi_low_dpi_displays()
            # NVIDIA: always remember user's selected mode
            # INTEL: only remember while in same display combination type
            #        When switching from hidpi-only to mixed-dpi or vice versa, set the appropriate default mode
            #        remember setting if eg, a user plugs a hidpi display into a hidpi laptop
            #        or if another display is plugged into an already mixed-dpi config.
            if self.get_gpu_vendor() == 'nvidia':
                pass
            elif not has_lowdpi and self.prev_display_types[2]:
                self.unforce = True
            elif has_mixed_dpi and not self.prev_display_types[0]:
                self.unforce = False
            self.set_scaled_display_modes()
        return False
    
    def run(self):
        # First set appropriate initial display configuration
        self.prev_display_types = self.has_mixed_hi_low_dpi_displays()
        if self.get_gpu_vendor() == 'nvidia':
            self.set_scaled_display_modes()
        elif not self.prev_display_types[2]:
            self.unforce = True
            self.set_scaled_display_modes()
        elif self.prev_display_types[0]:
            self.unforce = False
            self.set_scaled_display_modes()
        running = True
        prev_timestamp = 0
        while(running):
            # Get subscribed xlib RANDR events. Blocks until next event is received.
            e = self.xlib_display.next_event()
            # Multiple events are fired in quick succession, only act once.
            try:
                new_timestamp = e.timestamp
            except:
                new_timestamp = 0
            if new_timestamp > prev_timestamp:
                prev_timestamp = new_timestamp
                self.update(e)


def _run_hidpi_autoscaling(model):
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
            print(cmd)
            ##SubProcess.check_output(cmd)
            #subprocess.call('xrandr --addmode eDP-1 1600x900', shell=True)
        except:
            log.warning("Failed to add xrandr mode to display.")
    
    hidpi = HiDPIAutoscaling(model)
    hidpi.run()

    return hidpi

def run_hidpi_autoscaling(model):
    try:
        return _run_hidpi_autoscaling(model)
    except Exception:
        log.exception('Error calling _run_hidpi_autoscaling(%r):', model)
