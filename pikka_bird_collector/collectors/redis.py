import re

from .base_port_command import BasePortCommand, Base


class Redis(BasePortCommand):
    """
        Collector for Redis (http://redis.io/).
        
        This collector demonstrates one of the design principles of Pikka Bird,
        which is to be tolerant of multiple versions of services, attempting to
        parse their output and letting them control their own metrics names
        rather than forcing them to be called specific things. Rather than
        direct Redis bindings being used requiring an external dependency, or a
        direct socket connection, the +redis-cli+ command-line tool is used.
        
        The collector is enabled whenever non-empty settings are passed.
        
        DEPENDENCIES:
            redis-cli
                Available in PATH.
        
        SETTINGS:
            (minimal):
                {
                    6379: None}
            (supported):
                {
                    6379: {
                        'password':     "PASSWORD",
                        'cluster_info': False}}
        
        +AUTH+ support is provided via the settings.
        
        +CLUSTER INFO+ is merged into +INFO+, if the command succeeds, providing
        built-in support for Redis Cluster (3.0+).
        """
    
    COLLECT_SETTING_DEFAULTS = {
        'cluster_info': True}
    
    CMD_CLUSTER_INFO = 'CLUSTER INFO'
    CMD_INFO         = 'INFO'
    
    RE_SECTION = re.compile(r'# (?P<section>.+)')
    RE_SETTING = re.compile(r'(?P<k>\w+):(?P<v>.*)')
    
    @staticmethod
    def command_tool(port, settings, command):
        settings = settings or {}
        
        c = ['redis-cli', '-p', port]
        
        if settings.get('password'):
            c.extend(['-a', settings['password']])
        
        c.append(command)
        return c
    
    @staticmethod
    def parse_output(output, parse_opts={}):
        if output is None:
            return {}
        
        ds = {}
        
        section = None
        for row in output.split('\n'):
            m_section = Redis.RE_SECTION.match(row)
            if m_section:
                section = Base.parse_str_setting_key(m_section.group('section'))
                ds[section] = {}
            else:
                m_setting = Redis.RE_SETTING.match(row)
                if m_setting:
                    k = Base.parse_str_setting_key(m_setting.group('k'))
                    v = Base.parse_str_setting_value(m_setting.group('v'))
                    if section is None:
                        ds[k] = v
                    else:
                        ds[section][k] = v
        
        return ds
    
    def collect_port(self, port, settings):
        metrics = {}
        
        o = self.command_output(port, settings, self.CMD_INFO)
        ms = self.parse_output(o)
        
        if len(ms):
            metrics['info'] = ms
        else:
            return metrics # service down; give up
        
        if self.collect_setting('cluster_info', settings):
            o = self.command_output(port, settings, self.CMD_CLUSTER_INFO)
            ms = self.parse_output(o)
            
            if len(ms):
                metrics['cluster_info'] = ms
        
        return metrics
