from Xlib import X, display
from Xlib.ext import randr
from Xlib.protocol import rq, structs
import logging
import time

import subprocess
import re

from collections import namedtuple

log = logging.getLogger(__name__)

NEEDS_HIDPI_AUTOSCALING = (
    'bonw12',
    'galp2',
    'galp3',
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
    'galp3',
}

MODEL_MODES = {
    'galp2': '1600x900  118.25  1600 1696 1856 2112  900 903 908 934 -hsync +vsync',
    'galp3': '1600x900  118.25  1600 1696 1856 2112  900 903 908 934 -hsync +vsync',
}


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


XRes = namedtuple('XRes', ['x', 'y'])

class HiDPIAutoscaling:
    def __init__(self, model):
        self.model = model
        self.xrandr = ""
        self.displays = dict() # {'LVDS-0': 'connected', 'HDMI-0': 'disconnected'}
        self.display_modes = [] # Keep track of each display's X attributes
        self.dialog = None
        self.transfer_timeout = False
        self.panning_entries = []
        self.screen_maximum = XRes(x=8192, y=8192)
        self.active = True
        self.has_internal_hidpi = False
        self.pixel_doubling = False # If we have nvidia with the proprietary driver, set to True.
        
        self.init_xlib()
        
    def init_xlib(self):
        self.xlib_display = display.Display()
        screen = self.xlib_display.screen()
        self.xlib_window = screen.root.create_window(10,10,10,10,0, 0, window_class=X.InputOnly, visual=X.CopyFromParent, event_mask=0)
        self.xlib_window.xrandr_select_input(randr.RRScreenChangeNotifyMask
                    | randr.RROutputChangeNotifyMask
                    | randr.RROutputPropertyNotifyMask)

        resources = self.xlib_window.xrandr_get_screen_resources()._data
        for output in resources['outputs']:
                    info = dpi_get_output_info(self.xlib_display, output, resources['config_timestamp'])._data
                    
        self.update_display_connections()
        if self.get_gpu_vendor() == 'nvidia':
            self.pixel_doubling = True
            self.screen_maximum = XRes(x=32768, y=32768)

    #stub for now
    def get_gpu_vendor(self):
        return 'nvidia'
    
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
            
        for display in new_displays:
            status = new_displays[display]['connected']
            if display in self.displays:
                old_status = self.displays[display]['connected']
                if status != old_status:
                    self.displays = new_displays
                    return True
            else:
                self.displays = new_displays
                return True
        
        self.displays = new_displays
        return False
    
    def get_display_position(self, display_name):
        resources = self.xlib_window.xrandr_get_screen_resources()._data
        crtc = self.displays[display_name]['crtc']
        if crtc != 0:
            crtc_info = dpi_get_crtc_info(self.xlib_display, crtc, resources['config_timestamp'])._data
            return crtc_info['x'], crtc_info['y']
        else:
            return -1, -1
    
    def get_display_dpi(self, display_name):
        width = self.displays[display_name]['mm_width']
        height = self.displays[display_name]['mm_height']
        mode = self.displays[display_name]['modes'][0]
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
                            scale_factor =1
                            
                        if self.pixel_doubling == True:
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
                            
        return display_positions

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
        
        return attribute_mapping[display_name]


    def set_display_scaling_nvidia_settings(self, display_name, layout, force_hidpi=True):
        #DP-0: nvidia-auto-select @3840x2160 +0+0 {ViewPortIn=3840x2160, ViewPortOut=3840x2160+0+0, ForceCompositionPipeline=On}
        #DISPLAY_NAME
        #nvidia-auto-select
        #@panning res
        #+pan_x+pan_y
        #{ViewPortIn=,ViewPortOut=
        #other attributes from matched display
        #ForceCompositionPipeline=On}
        
        dpi = self.get_display_dpi(display_name)
        if dpi is None:
            return ''
        if force_hidpi == True:
            display_str = display_name + ": nvidia-auto-select "
            
            mode = self.displays[display_name]['modes'][0]
            res_out_x = mode['width']
            res_out_y = mode['height']
            
            if dpi > 170:
                res_in_x = mode['width']
                res_in_y = mode['height']
            else:
                res_in_x = 2 * mode['width']
                res_in_y = 2 * mode['height']
            pan_x, pan_y = layout[display_name]
            panning_pos = "+" + str(pan_x) + "+" + str(pan_y)
            
            viewportin = str(res_in_x) + "x" + str(res_in_y) + " "
            viewportout = str(res_out_x) + "x" + str(res_out_y) + panning_pos
            
            display_str = display_str + "@" + str(res_in_x) + "x" + str(res_in_y) + " "
            display_str = display_str + "+" + str(pan_x) + "+" + str(pan_y) + " "
            display_str = display_str + self.get_nvidia_settings_options(display_name, viewportin, viewportout)
            return display_str
            
            dpys = subprocess.check_output(['nvidia-settings', '-q', 'dpys'])
        
    
    def set_display_scaling(self, display, layout, force_lowdpi=False):
        if self.get_gpu_vendor() == 'nvidia':
            return self.set_display_scaling_nvidia_settings(display, layout, force_hidpi=True)
    
    def set_scaled_display_modes(self):
        layout = self.calculate_layout()
        cmd = ''
        for display in self.displays:
            if self.displays[display]['connected'] == True:
                pos_x, pos_y = self.get_display_position(display)
                dpi = self.get_display_dpi(display)
                cmd = cmd + self.set_display_scaling(display, layout)
        if self.get_gpu_vendor() == 'nvidia':
            subprocess.call('nvidia-settings --assign CurrentMetaMode="' + cmd + '"', shell=True)
        pass
    
    def run(self):
        running = True;
        last_time = time.time()
        while(running):
            # Get subscribed xlib RANDR events.  Multiple events are fired in quick succession, only act on first one.
            e = self.xlib_display.next_event()
            if time.time() - last_time > 1:
                last_time = time.time()
                if e.__class__.__name__ == randr.ScreenChangeNotify.__name__:
                    pass
                elif (e.type, e.sub_code) == self.xlib_display.extension_event.OutputChangeNotify:
                    #Do we ever get here???
                    e = randr.OutputChangeNotify(display=display.display, binarydata = e._binary)
                    running = False
                    
                time.sleep(.01)
                if self.update_display_connections():
                    self.set_scaled_display_modes()
                
def _run_hidpi_autoscaling(model):
    if model not in NEEDS_HIDPI_AUTOSCALING:
        log.info('Hidpi Autoscaling not needed for %r', model)
        return
    log.info('Hidpi autoscaling for %r', model)

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

    hidpi = HiDPIAutoscaling(model)
    hidpi.run()
    mainloop = GLib.MainLoop()
    mainloop.run()

    return hidpi

def run_hidpi_autoscaling(model):
    try:
        return _run_hidpi_autoscaling(model)
    except Exception:
        log.exception('Error calling _run_hidpi_autoscaling(%r):', model)
