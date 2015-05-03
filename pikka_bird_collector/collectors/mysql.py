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
                        'user':          "USER",
                        'password':      "PASSWORD",
                        'master_status': False,
                        'variables':     False}}
        """
    
    COLLECT_SETTING_DEFAULTS = {
        'master_status': True,
        'variables':     True}
    
    CMD_SHOW_MASTER_STATUS = 'SHOW MASTER STATUS'
    CMD_SHOW_STATUS        = 'SHOW /*!50002 GLOBAL */ STATUS'
    CMD_SHOW_VARIABLES     = 'SHOW VARIABLES'
    
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
    def parse_output_list(output, convert_bool=False):
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
    
    @staticmethod
    def parse_output_table(output, convert_bool=False):
        if output is None:
            return {}
        
        ds = {}
        
        rows   = [ r.split('\t') for r in output.split('\n') ]
        header = [ Base.parse_str_setting_key(k) for k in rows[0] ]
        
        for row in rows[1:]:
            if len(row) == len(header):
                k = Base.parse_str_setting_key(row[0])
                ds[k] = {}
                for i, v in enumerate(row[1:], start=1):
                    ds[k][header[i]] = Mysql.__parse_str_setting_value(v,
                        convert_bool)
        
        return ds
    
    def collect_port(self, port, settings):
        metrics = {}
        
        o = self.command_output(port, settings, self.CMD_SHOW_STATUS)
        ms = self.parse_output_list(o, convert_bool=True)
        
        if len(ms):
            metrics['status'] = ms
        else:
            return metrics # service down; give up
        
        if self.collect_setting('master_status', settings):
            o = self.command_output(port, settings, self.CMD_SHOW_MASTER_STATUS)
            ms = self.parse_output_table(o, convert_bool=True)
            
            if len(ms):
                metrics['master_status'] = ms
        
        if self.collect_setting('variables', settings):
            o = self.command_output(port, settings, self.CMD_SHOW_VARIABLES)
            ms = self.parse_output_list(o, convert_bool=True)
            
            if len(ms):
                metrics['variables'] = ms
        
        return metrics
    
    @staticmethod
    def __parse_str_setting_value(value, convert_bool):
        v = Base.parse_str_setting_value(value)
        
        if convert_bool and v in Mysql.PARSE_BOOLS:
            v = Mysql.PARSE_BOOLS[v]
        
        return v
