import re

from .base import Base


class Mysql(Base):
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
    def command_mysql(port, settings, command):
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
                k = m_setting.group('k').strip().lower()
                v = m_setting.group('v').strip()
                ds[k] = v
        
        return ds
    
    def enabled(self):
        return len(self.settings) >= 1
    
    def collect(self):
        metrics = {}
        
        return { port: self.__collect_port(port, settings)
            for port, settings in self.settings.items() }
    
    def __collect_port(self, port, settings):
        metrics = self.__command_parse_output(port, settings, 'SHOW VARIABLES')
        
        return metrics
    
    def __command_parse_output(self, port, settings, command):
        command_f = Mysql.command_mysql(port, settings, command)
        output = Base.exec_command(command_f)
        return Mysql.parse_output(output)
