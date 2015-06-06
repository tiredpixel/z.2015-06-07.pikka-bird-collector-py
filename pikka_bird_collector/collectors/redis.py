from pikka_bird_collector.parsers.redis import Redis as Parser
from .base_port_command import BasePortCommand, Base


class Redis(BasePortCommand):
    """
        Collector for Redis (http://redis.io/).
        
        The collector is enabled whenever non-empty settings are passed.
        Multiple instances running on the same box are supported; just specify
        each port within settings.
        
        By default, core status and cluster status are gathered.
        
        For consistency, `AUTH` is called `password`.
        
        DEPENDENCIES:
            redis-cli
                Available in PATH.
        
        SETTINGS:
            minimal:
                {
                    6379: None}
            supported:
                {
                    6379: {
                        'password': "PASSWORD",
                        'collect':  {
                            'cluster_info': False}}}
        
        +AUTH+ support is provided via the settings.
        
        +CLUSTER INFO+ is merged into +INFO+, if the command succeeds, providing
        built-in support for Redis Cluster (3.0+).
        """
    
    COLLECT_SETTING_DEFAULTS = {
        'cluster_info': True}
    
    CMD_CLUSTER_INFO = 'CLUSTER INFO'
    CMD_INFO         = 'INFO'
    
    @staticmethod
    def command_tool(port, settings, command):
        settings = settings or {}
        
        c = ['redis-cli', '-p', port]
        
        if settings.get('password'):
            c.extend(['-a', settings['password']])
        
        c.append(command)
        return c
    
    def collect_port(self, port, settings):
        metrics = {}
        
        parser = Parser(
            converter_key=Base.parse_str_setting_key,
            converter_value=Base.parse_str_setting_value)
        
        o = self.command_output(port, settings, self.CMD_INFO)
        ms = parser.parse(o)
        
        if len(ms):
            metrics['info'] = ms
        else:
            return metrics # service down; give up
        
        if self.collect_setting('cluster_info', settings):
            o = self.command_output(port, settings, self.CMD_CLUSTER_INFO)
            ms = parser.parse(o)
            
            if len(ms):
                metrics['cluster_info'] = ms
        
        return metrics
