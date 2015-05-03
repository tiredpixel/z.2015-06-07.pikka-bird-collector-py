import re

from .base_port_command import BasePortCommand, Base


class Mysql(BasePortCommand):
    """
        Collector for MySQL (http://redis.io/).
        
        The collector is enabled whenever non-empty settings are passed.
        
        DEPENDENCIES:
            mysql
                Available in PATH.
        
        SETTINGS:
            (minimal):
                {
                    3306: None}
            (supported):
                {
                    3306: {
                        'user': "USER",
                        'password': "PASSWORD"}}
        """
    
    RE_SETTING = re.compile(r'(?P<k>\w+)\t(?P<v>.*)')
    
    @staticmethod
    def command_tool(port, settings, command):
        settings = settings or {}
        
        c = ['mysql',
            '--host', '127.0.0.1', # socket not (yet) supported
            '--port', port,
            '--execute', command,
            '--batch',
            '--raw',
            '--skip-column-names']
        
        if settings.get('user'):
            c.append('--user=%s' % settings['user'])
        if settings.get('password'):
            c.append('--password=%s' % settings['password'])
        
        return c
    
    @staticmethod
    def parse_output(output):
        if output is None:
            return {}
        
        ds = {}
        
        for row in output.split('\n'):
            m_setting = Mysql.RE_SETTING.match(row)
            if m_setting:
                k = Base.parse_str_setting_key(m_setting.group('k'))
                v = Base.parse_str_setting_value(m_setting.group('v'))
                ds[k] = v
        
        return ds
    
    def collect_port(self, port, settings):
        metrics = self.command_parse_output(port, settings, 'SHOW VARIABLES')
        
        return metrics
