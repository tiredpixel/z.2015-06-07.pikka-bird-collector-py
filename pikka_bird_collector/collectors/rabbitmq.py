from pikka_bird_collector.parsers.erlang import Erlang as Parser
from .base_port_command import BasePortCommand, Base


class Rabbitmq(BasePortCommand):
    """
        Collector for RabbitMQ (https://www.rabbitmq.com).
        
        The collector is enabled whenever non-empty settings are passed.
        
        By default, core status and cluster status are gathered.
        
        For consistency, a port is required for this collector even though
        `rabbitmqctl` doesn't accept one, instead returning all information;
        this might change. [TODO review]
        
        This collector is slower than others, because of utilising a naïve
        Erlang data parser in Python. There might be a neater solution, or the
        parser could certainly be improved -- but it's likely good enough.
        
        Because of the difficulty in mapping Erlang structures to something
        suited to JSON, all 'values' are treated as arrays, with empty arrays
        changed to `None` and length-1 arrays unpacked. This gives sensible
        results in most cases, but be aware. :)
        
        DEPENDENCIES:
            rabbitmqctl
                Available in PATH.
        
        SETTINGS:
            minimal:
                {
                    5672: None}
            supported:
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
    
    def collect_port(self, port, settings):
        metrics = {}
        
        parser = Parser()
        
        o = self.command_output(port, settings, self.CMD_STATUS)
        ms = parser.parse(o)
        
        if len(ms):
            metrics['status'] = ms
        else:
            return metrics # service down; give up
        
        if self.collect_setting('cluster_status', settings):
            o = self.command_output(port, settings, self.CMD_CLUSTER_STATUS)
            ms = parser.parse(o)
            
            if len(ms):
                metrics['cluster_status'] = ms
        
        return metrics
