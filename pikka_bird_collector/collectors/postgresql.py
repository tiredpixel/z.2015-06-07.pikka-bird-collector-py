import re

from .base_port_command import BasePortCommand, Base


class Postgresql(BasePortCommand):
    """
        Collector for PostgreSQL (http://www.postgresql.org/).
        
        The collector is enabled whenever non-empty settings are passed.
        
        DEPENDENCIES:
            psql
                Available in PATH.
        
        SETTINGS:
            (minimal):
                {
                    5432: None}
            (supported):
                {
                    5432: {
                        'user':             "USER",
                        'stat_replication': False,
                        'settings':         False}}
        """
    
    COLLECT_SETTING_DEFAULTS = {
        'stat_replication': True,
        'settings':         True}
    
    CMD_STATUS = """
        SELECT
          inet_client_addr(),
          inet_client_port(),
          inet_server_addr(),
          inet_server_port(),
          pg_backend_pid(),
          pg_backup_start_time(),
          pg_conf_load_time(),
          (CASE pg_is_in_backup()
            WHEN 'f' THEN pg_current_xlog_insert_location()
            END) AS pg_current_xlog_insert_location,
          (CASE pg_is_in_backup()
            WHEN 'f' THEN pg_current_xlog_location()
            END) AS pg_current_xlog_location,
          (CASE pg_is_in_backup()
            WHEN 't' THEN 'on'
            WHEN 'f' THEN 'off'
            END) AS pg_is_in_backup,
          (CASE pg_is_in_recovery()
            WHEN 't' THEN 'on'
            WHEN 'f' THEN 'off'
            END) AS pg_is_in_recovery,
          (CASE pg_is_in_recovery()
            WHEN 't' THEN (CASE pg_is_xlog_replay_paused()
                            WHEN 't' THEN 'on'
                            WHEN 'f' THEN 'off'
                            END)
            END) AS pg_is_xlog_replay_paused,
          pg_last_xact_replay_timestamp(),
          pg_last_xlog_receive_location(),
          pg_last_xlog_replay_location(),
          pg_postmaster_start_time(),
          extract(epoch from (now() - pg_postmaster_start_time())) AS uptime_s,
          version()
        """.replace('\n', ' ')
    CMD_SETTINGS         = 'SELECT name, setting FROM pg_settings'
    CMD_STAT_REPLICATION = 'SELECT * FROM pg_stat_replication'
    
    PARSE_BOOLS = {
        'on':  True,
        'off': False}
    
    @staticmethod
    def command_tool(port, settings, command):
        settings = settings or {}
        
        c = []
        
        c.extend(['psql',
            '--host', '127.0.0.1', # socket not (yet) supported
            '--port', port,
            '--dbname', 'template1',
            '--command', command,
            '--no-password',
            '--quiet',
            '--no-align',
            '--pset=footer=off'])
        
        if settings.get('user'):
            c.append('--username=%s' % settings['user'])
        
        return c
    
    @staticmethod
    def parse_output(output, convert_bool=False, tr=False):
        if output is None:
            return {}
        
        ds = {}
        
        rows   = [ r.split('|') for r in output.split('\n') ]
        header = [ Base.parse_str_setting_key(k) for k in rows[0] ]
        
        for row in rows[1:]:
            if len(row) == len(header):
                if tr == True:
                    for i, v in enumerate(row):
                        k = Base.parse_str_setting_key(header[i])
                        ds[k] = Postgresql.__parse_str_setting_value(v,
                            convert_bool)
                elif tr == 2:
                    k = Base.parse_str_setting_key(row[0])
                    ds[k] = Postgresql.__parse_str_setting_value(row[1],
                        convert_bool)
                    
                else:
                    k = Base.parse_str_setting_key(row[0])
                    ds[k] = {}
                    for i, v in enumerate(row[1:], start=1):
                        ds[k][header[i]] = Postgresql.__parse_str_setting_value(v,
                            convert_bool)
        
        return ds
    
    def collect_port(self, port, settings):
        metrics = {}
        
        o = self.command_output(port, settings, self.CMD_STATUS)
        ms = self.parse_output(o, convert_bool=True, tr=True)
        
        if len(ms):
            metrics['status'] = ms
        else:
            return metrics # service down; give up
        
        if self.collect_setting('stat_replication', settings):
            o = self.command_output(port, settings, self.CMD_STAT_REPLICATION)
            ms = self.parse_output(o, convert_bool=True)
            
            if len(ms):
                metrics['stat_replication'] = ms
        
        if self.collect_setting('settings', settings):
            o = self.command_output(port, settings, self.CMD_SETTINGS)
            ms = self.parse_output(o, convert_bool=True, tr=2)
            
            if len(ms):
                metrics['settings'] = ms
        
        return metrics
    
    @staticmethod
    def __parse_str_setting_value(value, convert_bool):
        v = Base.parse_str_setting_value(value)
        
        if convert_bool and v in Postgresql.PARSE_BOOLS:
            v = Postgresql.PARSE_BOOLS[v]
        
        return v
