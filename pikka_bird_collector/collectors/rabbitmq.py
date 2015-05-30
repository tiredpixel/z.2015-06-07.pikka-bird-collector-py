import json
import re

from .base_port_command import BasePortCommand, Base


class Rabbitmq(BasePortCommand):
    """
        Collector for RabbitMQ (https://www.rabbitmq.com).
        
        The collector is enabled whenever non-empty settings are passed.
        
        DEPENDENCIES:
            rabbitmqctl
                Available in PATH.
        
        SETTINGS:
            (minimal):
                {
                    5672: None}
            (supported):
                {
                    5672: {
                        'collect': {
                            'cluster_status': False}}}
        """
    
    COLLECT_SETTING_DEFAULTS = {
        'cluster_status': True}
    
    CMD_STATUS         = 'status'
    CMD_CLUSTER_STATUS = 'cluster_status'
    
    @staticmethod
    def command_tool(port, settings, command):
        settings = settings or {}
        
        c = ['rabbitmqctl',
            '-q',
            command]
        
        return c
    
    @staticmethod
    def parse_output(output, parse_opts={}):
        if output is None:
            return {}
        
        d = {}
        
        buf        = ''
        depth      = 0
        emit_buf   = None
        emit_depth = []
        emit_t     = None
        i          = 0
        in_q       = -1
        in_s       = 's'
        
        def o_r(i):
            if i < len(output):
                return output[i]
        
        def o_r_s(i):
            c = o_r(i)
            while c in [' ', '\n', '}']:
                i += 1
                c = o_r(i)
            return i, c
        
        def d_update(d, k, v):
            if len(k) == 1:
                d[k[0]] = v
                return d
            else:
                k2 = k.pop()
                if k2 not in d:
                    d[k2] = {}
                return d_update(d[k2], k, v)
        
        def emit(depth, in_s, buf, d, emit_buf, emit_depth):
            if in_s == 'k':
                buf = buf.strip()
                if len(emit_depth) > depth:
                    emit_depth[depth] = buf
                else:
                    emit_depth.append(buf)
                emit_depth = emit_depth[:(depth + 1)]
                emit_buf = [buf]
            elif in_s == 'v':
                buf = re.sub(r'<<"(.*)">>', r'"\g<1>"', buf)
                try:
                    buf = json.loads('[' + buf + ']')
                except ValueError:
                    buf = buf.split(',')
                if len(buf) == 0:
                    buf = None
                elif len(buf) == 1:
                    buf = buf[0]
                emit_buf.append(buf)
                d_update(d, emit_depth[::-1], buf)
            return d, emit_buf, emit_depth
        
        while i < len(output):
            if in_s == 's':
                i, c = o_r_s(i)
                if c == '[':
                    i += 1
                    i, c = o_r_s(i)
                    if c == '{':
                        in_s = 'k'
                elif c == '{':
                    in_s = 'k'
            elif in_s == 'k':
                i, c = o_r_s(i)
                if c == ',':
                    if emit_t == 'k':
                        depth += 1
                    emit_t = 'k'
                    d, emit_buf, emit_depth = emit(depth, in_s, buf, d, emit_buf, emit_depth)
                    in_s = 'v'
                    buf = ''
                else:
                    buf += c
            elif in_s == 'v':
                c = o_r(i)
                if c == '"':
                    in_q *= -1
                if in_q == -1 and c in ['}', ']']:
                    if emit_t == 'k':
                        d, emit_buf, emit_depth = emit(depth, in_s, buf, d, emit_buf, emit_depth)
                    emit_t = 'v'
                    buf = ''
                    i += 1
                    i, c = o_r_s(i)
                    if c == ',':
                        in_s = 's'
                    elif c == ']':
                        depth -= 1
                elif in_q == -1 and c == '[':
                    i += 1
                    c = o_r(i)
                    if c == '{':
                        in_s = 's'
                    i -= 1
                else:
                    if in_q == 1 or buf != '' or c != '{':
                        buf += c
            i += 1
        
        emit(depth + 1, 'k', buf, d, emit_buf, emit_depth)
        
        return d
    
    def collect_port(self, port, settings):
        metrics = {}
        
        o = self.command_output(port, settings, self.CMD_STATUS)
        ms = self.parse_output(o)
        
        if len(ms):
            metrics['status'] = ms
        else:
            return metrics # service down; give up
        
        if self.collect_setting('cluster_status', settings):
            o = self.command_output(port, settings, self.CMD_CLUSTER_STATUS)
            ms = self.parse_output(o)
            
            if len(ms):
                metrics['cluster_status'] = ms
        
        return metrics
