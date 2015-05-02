import re

from .base import Base


class Redis(Base):
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
                        'password': "PASSWORD"}}
        
        +AUTH+ support is provided via the settings.
        
        +CLUSTER INFO+ is merged into +INFO+, if the command succeeds, providing
        built-in support for Redis Cluster (3.0+).
        """
    
    RE_SECTION = re.compile(r'# (?P<section>.+)')
    RE_SETTING = re.compile(r'(?P<k>\w+):(?P<v>.*)')
    
    @staticmethod
    def command_redis(port, settings, command):
        settings = settings or {}
        
        c = ['redis-cli', '-p', port]
        
        if settings.get('password'):
            c.extend(['-a', settings['password']])
        
        c.append(command)
        return c
    
    @staticmethod
    def parse_output(output):
        if output is None:
            return {}
        
        ds = {}
        
        section = None
        for row in output.split('\n'):
            m_section = Redis.RE_SECTION.match(row)
            if m_section:
                section = m_section.group('section').strip().lower()
                ds[section] = {}
            else:
                m_setting = Redis.RE_SETTING.match(row)
                if m_setting:
                    k = m_setting.group('k').strip().lower()
                    v = m_setting.group('v').strip()
                    if section is None:
                        ds[k] = v
                    else:
                        ds[section][k] = v
        
        return ds
    
    def enabled(self):
        return len(self.settings) >= 1
    
    def collect(self):
        metrics = {}
        
        return { port: self.__collect_port(port, settings)
            for port, settings in self.settings.items() }
    
    def __collect_port(self, port, settings):
        metrics = self.__command_parse_output(port, settings, 'INFO')
        
        ms = self.__command_parse_output(port, settings, 'CLUSTER INFO')
        
        if len(ms):
            metrics['cluster'] = metrics.get('cluster') or {}
            metrics['cluster'].update(ms)
        
        return metrics
    
    def __command_parse_output(self, port, settings, command):
        command_f = Redis.command_redis(port, settings, command)
        output = Base.exec_command(command_f)
        return Redis.parse_output(output)
