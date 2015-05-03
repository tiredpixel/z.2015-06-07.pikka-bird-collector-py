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
    
    CMD_SHOW_STATUS    = 'SHOW /*!50002 GLOBAL */ STATUS'
    CMD_SHOW_VARIABLES = 'SHOW VARIABLES'
    
    RE_SETTING = re.compile(r'(?P<k>\w+)\t(?P<v>.*)')
    
    PARSE_BOOLS = {
        'ON':  True,
        'OFF': False,
        'YES': True,
        'NO':  False}
    
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
    def parse_output(output, convert_bool=False):
        if output is None:
            return {}
        
        ds = {}
        
        for row in output.split('\n'):
            m_setting = Mysql.RE_SETTING.match(row)
            if m_setting:
                k = Base.parse_str_setting_key(m_setting.group('k'))
                v = Mysql.__parse_str_setting_value(m_setting.group('v'),
                    convert_bool)
                ds[k] = v
        
        return ds
    
    def collect_port(self, port, settings):
        metrics = {}
        
        o = self.command_output(port, settings, self.CMD_SHOW_STATUS)
        ms = self.parse_output(o, convert_bool=True)
        
        if len(ms):
            metrics['status'] = ms
        else:
            return metrics # service down; give up
        
        o = self.command_output(port, settings, self.CMD_SHOW_VARIABLES)
        ms = self.parse_output(o, convert_bool=True)
        
        if len(ms):
            metrics['variables'] = ms
        
        return metrics
    
    @staticmethod
    def __parse_str_setting_value(value, convert_bool):
        v = Base.parse_str_setting_value(value)
        
        if convert_bool and v in Mysql.PARSE_BOOLS:
            v = Mysql.PARSE_BOOLS[v]
        
        return v
