#!/usr/bin/python3

class MonitorsXml():
    def __init__(self):
        lines = []
        self.state = []
        
        try:
            fp = open('.config/monitors.xml', 'r')
        except:
            self.monitors = []
            return
        line = fp.readline()
        while line:
            line_type = self.getLineType(line.lstrip())
            lines.append(line_type)
            line = fp.readline()
        
        for line in lines:
            self.process_state(line)
            
    def getLineType(self, line):
        if len(line) < 1:
            return None
        has_close = False
        has_end_caret = False
        has_tag = False
        complete = False
        # Lines may have three parts: <opening-tag>contents</closing-tag>
        
        # Get opening or closing tag
        if line[0] == '<':
            idx = 0
            for c in line:
                idx = idx + 1
                if idx == 2 and c == '/':   # tag is closing tag
                    has_close = True
                if c == ' ':                # tag has properties
                    has_tag = True
                    tag = line[1:idx-1]
                if c == '>':                # found end of tag
                    if not has_tag:
                        if has_close:
                            tag = line[2:idx-1]
                        else:
                            tag = line[1:idx-1]
                    has_end_caret = True
                    remaining_line = line[idx:]
                    break
            
            # Get contents if line isn't finished
            idx = 0
            for c in remaining_line:
                idx = idx + 1
                if c == '<':
                    contents = remaining_line[0:idx-1]
                    remaining_line = remaining_line[idx:]
            
            # Get closing tag if line isn't finished
            idx = 0
            for c in remaining_line:
                idx = idx + 1
                if idx == 2 and c == '/':
                    has_close = True
                if c == ' ':
                    has_tag = True
                    tag = line[1:idx]
                if c == '>':
                    if not has_tag:
                        if has_close:
                            tag = remaining_line[2:idx-1]
                        else:
                            tag = line[1:idx-1]
                    has_end_caret = True
                    if contents:
                        complete = True
                    break
            
            # Return which type of line we read for processing 
            if complete:
                return 'complete', tag, contents
            if has_end_caret and has_close:
                return 'close', tag, None
            elif has_end_caret:
                return 'open', tag, None
            else:
                return 'nope'
    
    def process_state(self, line):
        #line_type = line[0]
        tag = line[1]
        contents = line[2]
        
        # track state we are in based on recieved tags.
        # Only process recognized tags.
        if line[0] == 'open':
            self.state.append(line[1])
            if tag == 'monitors':
                self.monitors = []
            if tag == 'configuration':
                self.configuration = {'logical_monitors': []}
            if tag == 'logicalmonitor':
                self.logical_monitor = {'monitor_spec': {}, 'mode': {}}
            if tag == 'monitorspec':
                self.monitor_spec = {}
            if tag == 'mode':
                self.mode = {}
        elif line[0] == 'close':
            self.state.pop()
            if tag == 'configuration':
                self.monitors.append(self.configuration)
            if tag == 'logicalmonitor':
                self.configuration['logical_monitors'].append(self.logical_monitor)
            if tag == 'monitorspec':
                self.logical_monitor['monitor_spec'] = self.monitor_spec
            if tag == 'mode':
                self.logical_monitor['mode'] = self.mode
        else:
            state = self.state.pop()
            self.state.append(state)
            if state == 'logicalmonitor':
                self.logical_monitor[tag] = contents
            elif state == 'monitorspec':
                self.monitor_spec[tag] = contents
            elif state == 'mode':
                self.mode[tag] = contents
    
    def get_config_from_monitors(self, monitor_list):
        # compare monitor list to configurations in monitors.xml
        # if there exists a configuration that matches connector, vendor, product, and serial for every monitor in the list,
        # return that configuration
        
        for config in self.monitors:
            miss = False
            connections = {}
            for mon in monitor_list:
                if mon['connector'] not in connections:
                    connections[mon['connector']] = {}
                connections[mon['connector']]['edid_vendor'] = mon['vendor']
                connections[mon['connector']]['edid_product'] = mon['product']
                connections[mon['connector']]['edid_serial'] = mon['serial']
            for log in config['logical_monitors']:
                if log['monitor_spec']['connector'] not in connections:
                    connections[log['monitor_spec']['connector']] = {}
                connections[log['monitor_spec']['connector']]['spec_vendor'] = log['monitor_spec']['vendor']
                connections[log['monitor_spec']['connector']]['spec_product'] = log['monitor_spec']['product']
                connections[log['monitor_spec']['connector']]['spec_serial'] = log['monitor_spec']['serial']
            for connection in connections:
                for key in ['edid_vendor', 'edid_product', 'edid_serial', 'spec_vendor', 'spec_product', 'spec_serial']:
                    if key not in connections[connection]:
                        miss = True
                if miss == False:
                    if connections[connection]['spec_vendor'] != connections[connection]['edid_vendor']:
                        miss = True
                    if connections[connection]['spec_product'] != connections[connection]['edid_product']:
                        miss = True
                    if connections[connection]['spec_serial'] != connections[connection]['edid_serial']:
                        miss = True
                    
            if miss == False:
                return config
        return None
        
