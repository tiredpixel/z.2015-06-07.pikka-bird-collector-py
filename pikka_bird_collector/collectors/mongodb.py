import json
import re

from .base_port_command import BasePortCommand, Base


class Mongodb(BasePortCommand):
    """
        Collector for MongoDB (https://www.mongodb.org/).
        
        The collector is enabled whenever non-empty settings are passed.
        Multiple instances running on the same box are supported; just specify
        each port within settings.
        
        By default, core status and replication status are gathered.
        
        Note that this collector imports metrics keys unmodified, so most keys
        use camelcase; this might change. [TODO review]
        
        DEPENDENCIES:
            mongo
                Available in PATH.
        
        SETTINGS:
            minimal:
                {
                    27017: None}
            supported:
                {
                    27017: {
                        'user':     "USER",
                        'password': "PASSWORD",
                        'collect':  {
                            'rs_status': False}}}
        """
    
    COLLECT_SETTING_DEFAULTS = {
        'rs_status': True}
    
    CMD_DB_SERVER_STATUS = 'printjson(db.serverStatus())'
    CMD_RS_STATUS        = 'printjson(rs.status())'
    
    RE_UNOBJECTS = [
        re.compile(r'\b(?:Date|ISODate|NumberInt|NumberLong|ObjectId)\((.*?)\)'),
        re.compile(r'\bTimestamp\(\s*(\d+)\s*,\s*\d+\s*\)')]
    
    @staticmethod
    def command_tool(port, settings, command):
        settings = settings or {}
        
        c = []
        
        c.extend(['mongo',
            '--port', port,
            '--eval', command,
            '--quiet'])
        
        if settings.get('user'):
            c.extend(['--username', settings['user']])
        
        if settings.get('password'):
            c.extend(['--password', settings['password']])
        
        return c
    
    @staticmethod
    def parse_output(output, parse_opts={}):
        if output is None:
            return {}
        
        for re_object in Mongodb.RE_UNOBJECTS:
            output = re_object.sub(r'\g<1>', output)
        
        return json.loads(output)
    
    def collect_port(self, port, settings):
        metrics = {}
        
        o = self.command_output(port, settings, self.CMD_DB_SERVER_STATUS)
        ms = self.parse_output(o)
        
        if len(ms):
            metrics['server_status'] = ms
        else:
            return metrics # service down; give up
        
        if self.collect_setting('rs_status', settings):
            o = self.command_output(port, settings, self.CMD_RS_STATUS)
            ms = self.parse_output(o)
            
            if len(ms):
                metrics['rs_status'] = ms
        
        return metrics
