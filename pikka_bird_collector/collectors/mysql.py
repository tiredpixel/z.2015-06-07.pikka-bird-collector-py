import pikka_bird_collector.parsers as parsers
from .base_port_command import BasePortCommand, Base


class Mysql(BasePortCommand):
    """
        Collector for MySQL (https://www.mysql.com/).
        
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
                        'slave_status':  False,
                        'slave_hosts':   False,
                        'variables':     False}}
        """
    
    COLLECT_SETTING_DEFAULTS = {
        'master_status': True,
        'slave_hosts':   True,
        'slave_status':  True,
        'variables':     True}
    
    CMD_SHOW_MASTER_STATUS = 'SHOW MASTER STATUS'
    CMD_SHOW_SLAVE_HOSTS   = 'SHOW SLAVE HOSTS'
    CMD_SHOW_SLAVE_STATUS  = 'SHOW SLAVE STATUS'
    CMD_SHOW_STATUS        = 'SHOW /*!50002 GLOBAL */ STATUS'
    CMD_SHOW_VARIABLES     = 'SHOW VARIABLES'
    
    PARSE_BOOLS = { # the stringy booleans are inconsistent
        'ON':  True,
        'OFF': False,
        'YES': True,
        'NO':  False,
        'Yes': True,
        'No':  False}
    
    @staticmethod
    def command_tool(port, settings, command):
        settings = settings or {}
        
        c = ['mysql',
            '--host', '127.0.0.1', # socket not (yet) supported
            '--port', port,
            '--execute', command,
            '--batch',
            '--raw',
            '--column-names']
        
        if settings.get('user'):
            c.append('--user=%s' % settings['user'])
        if settings.get('password'):
            c.append('--password=%s' % settings['password'])
        
        return c
    
    def collect_port(self, port, settings):
        metrics = {}
        
        o = self.command_output(port, settings, self.CMD_SHOW_STATUS)
        ms = parsers.table(o,
            converter_key=Base.parse_str_setting_key,
            converter_value=Mysql.__parse_str_setting_value)
        
        if len(ms):
            metrics['status'] = ms
        else:
            return metrics # service down; give up
        
        if self.collect_setting('master_status', settings):
            o = self.command_output(port, settings, self.CMD_SHOW_MASTER_STATUS)
            ms = parsers.table(o,
                converter_key=Base.parse_str_setting_key,
                converter_value=Mysql.__parse_str_setting_value,
                tag_header_col='file')
            
            if len(ms):
                metrics['master_status'] = ms
        
        if self.collect_setting('slave_status', settings):
            o = self.command_output(port, settings, self.CMD_SHOW_SLAVE_STATUS)
            ms = parsers.table(o,
                converter_key=Base.parse_str_setting_key,
                converter_value=Mysql.__parse_str_setting_value,
                transpose=True)
            
            if len(ms):
                metrics['slave_status'] = ms
        
        if self.collect_setting('slave_hosts', settings):
            o = self.command_output(port, settings, self.CMD_SHOW_SLAVE_HOSTS)
            ms = parsers.table(o,
                converter_key=Base.parse_str_setting_key,
                converter_value=Mysql.__parse_str_setting_value,
                tag_header_col='server_id')
            
            if len(ms):
                metrics['slave_hosts'] = ms
        
        if self.collect_setting('variables', settings):
            o = self.command_output(port, settings, self.CMD_SHOW_VARIABLES)
            ms = parsers.table(o,
                converter_key=Base.parse_str_setting_key,
                converter_value=Mysql.__parse_str_setting_value)
            
            if len(ms):
                metrics['variables'] = ms
        
        return metrics
    
    @staticmethod
    def __parse_str_setting_value(value):
        v = Base.parse_str_setting_value(value)
        
        if v in Mysql.PARSE_BOOLS:
            v = Mysql.PARSE_BOOLS[v]
        
        return v
