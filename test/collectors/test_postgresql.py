import os

from pikka_bird_collector.collectors.postgresql import Postgresql
from pikka_bird_collector.collectors.base_port_command import BasePortCommand


class TestPostgresql:
    
    @staticmethod
    def fixture_path(filename):
        return os.path.join(os.path.dirname(__file__), '../fixtures', filename)
    
    @staticmethod
    def read_fixture(filename):
        with open(filename, 'r') as f_h:
            d = f_h.read()
        return d
    
    def mock_cmd_status(self):
        f = TestPostgresql.fixture_path('postgresql/status.txt')
        return TestPostgresql.read_fixture(f)
    
    def mock_cmd_stat_replication(self):
        f = TestPostgresql.fixture_path('postgresql/stat_replication.txt')
        return TestPostgresql.read_fixture(f)
    
    def mock_cmd_settings(self):
        f = TestPostgresql.fixture_path('postgresql/settings.txt')
        return TestPostgresql.read_fixture(f)
    
    def mock_exec_command(self, command_f):
        if Postgresql.CMD_STATUS in command_f:
            return self.mock_cmd_status()
        elif Postgresql.CMD_STAT_REPLICATION in command_f:
            return self.mock_cmd_stat_replication()
        elif Postgresql.CMD_SETTINGS in command_f:
            return self.mock_cmd_settings()
    
    def mock_collect_status(self):
        return {
            'inet_client_addr': '127.0.0.1',
            'inet_client_port': 53666,
            'inet_server_addr': '127.0.0.1',
            'inet_server_port': 5432,
            'pg_backend_pid': 28262,
            'pg_backup_start_time': None,
            'pg_conf_load_time': '2015-05-09 13:06:08.690997+01',
            'pg_current_xlog_insert_location': '0/308A8CE0',
            'pg_current_xlog_location': '0/308A8CE0',
            'pg_is_in_backup': False,
            'pg_is_in_recovery': False,
            'pg_is_xlog_replay_paused': None,
            'pg_last_xact_replay_timestamp': None,
            'pg_last_xlog_receive_location': None,
            'pg_last_xlog_replay_location': None,
            'pg_postmaster_start_time': '2015-05-09 13:06:08.858083+01',
            'uptime_s': 16227.606185,
            'version': 'PostgreSQL 9.4.1 on x86_64-apple-darwin14.3.0, compiled by Apple LLVM version 6.1.0 (clang-602.0.49) (based on LLVM 3.6.0svn), 64-bit'}
    
    def mock_collect_stat_replication(self):
        return {
            '1114': {
                'application_name': 'walreceiver',
                'backend_start': '15-MAY-14 19:54:05.535695 -04:00',
                'backend_xmin': None,
                'client_addr': '127.0.0.1',
                'client_hostname': None,
                'client_port': 52444,
                'flush_location': '0/290044C0',
                'pid': 1114,
                'replay_location': '0/290044C0',
                'sent_location': '0/290044C0',
                'state': 'streaming',
                'sync_priority': 0,
                'sync_state': 'async',
                'usename': 'repuser',
                'usesysid': 16384,
                'write_location': '0/290044C0'}}
    
    def mock_collect_settings(self):
        return {
            'allow_system_table_mods': False,
            'application_name': 'psql',
            'archive_command': '(disabled)',
            'archive_mode': False,
            'archive_timeout': 0,
            'array_nulls': True,
            'authentication_timeout': 60,
            'autovacuum': True,
            'autovacuum_analyze_scale_factor': 0.1,
            'autovacuum_analyze_threshold': 50,
            'autovacuum_freeze_max_age': 200000000,
            'autovacuum_max_workers': 3,
            'autovacuum_multixact_freeze_max_age': 400000000,
            'autovacuum_naptime': 60,
            'autovacuum_vacuum_cost_delay': 20,
            'autovacuum_vacuum_cost_limit': -1,
            'autovacuum_vacuum_scale_factor': 0.2,
            'autovacuum_vacuum_threshold': 50,
            'autovacuum_work_mem': -1,
            'backslash_quote': 'safe_encoding',
            'bgwriter_delay': 200,
            'bgwriter_lru_maxpages': 100,
            'bgwriter_lru_multiplier': 2,
            'block_size': 8192,
            'bonjour': False,
            'bonjour_name': None,
            'bytea_output': 'hex',
            'check_function_bodies': True,
            'checkpoint_completion_target': 0.5,
            'checkpoint_segments': 3,
            'checkpoint_timeout': 300,
            'checkpoint_warning': 30,
            'client_encoding': 'UTF8',
            'client_min_messages': 'notice',
            'commit_delay': 0,
            'commit_siblings': 5,
            'config_file': '/usr/local/var/postgres/postgresql.conf',
            'constraint_exclusion': 'partition',
            'cpu_index_tuple_cost': 0.005,
            'cpu_operator_cost': 0.0025,
            'cpu_tuple_cost': 0.01,
            'cursor_tuple_fraction': 0.1,
            'data_checksums': False,
            'data_directory': '/usr/local/var/postgres',
            'datestyle': 'ISO, DMY',
            'db_user_namespace': False,
            'deadlock_timeout': 1000,
            'debug_assertions': False,
            'debug_pretty_print': True,
            'debug_print_parse': False,
            'debug_print_plan': False,
            'debug_print_rewritten': False,
            'default_statistics_target': 100,
            'default_tablespace': None,
            'default_text_search_config': 'pg_catalog.english',
            'default_transaction_deferrable': False,
            'default_transaction_isolation': 'read committed',
            'default_transaction_read_only': False,
            'default_with_oids': False,
            'dynamic_library_path': '$libdir',
            'dynamic_shared_memory_type': 'posix',
            'effective_cache_size': 524288,
            'effective_io_concurrency': 0,
            'enable_bitmapscan': True,
            'enable_hashagg': True,
            'enable_hashjoin': True,
            'enable_indexonlyscan': True,
            'enable_indexscan': True,
            'enable_material': True,
            'enable_mergejoin': True,
            'enable_nestloop': True,
            'enable_seqscan': True,
            'enable_sort': True,
            'enable_tidscan': True,
            'escape_string_warning': True,
            'event_source': 'PostgreSQL',
            'exit_on_error': False,
            'external_pid_file': None,
            'extra_float_digits': 0,
            'from_collapse_limit': 8,
            'fsync': True,
            'full_page_writes': True,
            'geqo': True,
            'geqo_effort': 5,
            'geqo_generations': 0,
            'geqo_pool_size': 0,
            'geqo_seed': 0,
            'geqo_selection_bias': 2,
            'geqo_threshold': 12,
            'gin_fuzzy_search_limit': 0,
            'hba_file': '/usr/local/var/postgres/pg_hba.conf',
            'hot_standby': False,
            'hot_standby_feedback': False,
            'huge_pages': 'try',
            'ident_file': '/usr/local/var/postgres/pg_ident.conf',
            'ignore_checksum_failure': False,
            'ignore_system_indexes': False,
            'integer_datetimes': True,
            'intervalstyle': 'postgres',
            'join_collapse_limit': 8,
            'krb_caseins_users': False,
            'krb_server_keyfile': 'FILE:/usr/local/Cellar/postgresql/9.4.1_1/etc/krb5.keytab',
            'lc_collate': 'en_GB.UTF-8',
            'lc_ctype': 'en_GB.UTF-8',
            'lc_messages': 'en_GB.UTF-8',
            'lc_monetary': 'en_GB.UTF-8',
            'lc_numeric': 'en_GB.UTF-8',
            'lc_time': 'en_GB.UTF-8',
            'listen_addresses': 'localhost',
            'lo_compat_privileges': False,
            'local_preload_libraries': None,
            'lock_timeout': 0,
            'log_autovacuum_min_duration': -1,
            'log_checkpoints': False,
            'log_connections': False,
            'log_destination': 'stderr',
            'log_directory': 'pg_log',
            'log_disconnections': False,
            'log_duration': False,
            'log_error_verbosity': 'default',
            'log_executor_stats': False,
            'log_file_mode': 600,
            'log_filename': 'postgresql-%Y-%m-%d_%H%M%S.log',
            'log_hostname': False,
            'log_line_prefix': None,
            'log_lock_waits': False,
            'log_min_duration_statement': -1,
            'log_min_error_statement': 'error',
            'log_min_messages': 'warning',
            'log_parser_stats': False,
            'log_planner_stats': False,
            'log_rotation_age': 1440,
            'log_rotation_size': 10240,
            'log_statement': 'none',
            'log_statement_stats': False,
            'log_temp_files': -1,
            'log_timezone': 'GB',
            'log_truncate_on_rotation': False,
            'logging_collector': False,
            'maintenance_work_mem': 65536,
            'max_connections': 100,
            'max_files_per_process': 1000,
            'max_function_args': 100,
            'max_identifier_length': 63,
            'max_index_keys': 32,
            'max_locks_per_transaction': 64,
            'max_pred_locks_per_transaction': 64,
            'max_prepared_transactions': 0,
            'max_replication_slots': 0,
            'max_stack_depth': 2048,
            'max_standby_archive_delay': 30000,
            'max_standby_streaming_delay': 30000,
            'max_wal_senders': 0,
            'max_worker_processes': 8,
            'password_encryption': True,
            'port': 5432,
            'post_auth_delay': 0,
            'pre_auth_delay': 0,
            'quote_all_identifiers': False,
            'random_page_cost': 4,
            'restart_after_crash': True,
            'search_path': '"$user",public',
            'segment_size': 131072,
            'seq_page_cost': 1,
            'server_encoding': 'UTF8',
            'server_version': '9.4.1',
            'server_version_num': 90401,
            'session_preload_libraries': None,
            'session_replication_role': 'origin',
            'shared_buffers': 16384,
            'shared_preload_libraries': None,
            'sql_inheritance': True,
            'ssl': False,
            'ssl_ca_file': None,
            'ssl_cert_file': 'server.crt',
            'ssl_ciphers': 'HIGH:MEDIUM:+3DES:!aNULL',
            'ssl_crl_file': None,
            'ssl_ecdh_curve': 'prime256v1',
            'ssl_key_file': 'server.key',
            'ssl_prefer_server_ciphers': True,
            'ssl_renegotiation_limit': 524288,
            'standard_conforming_strings': True,
            'statement_timeout': 0,
            'stats_temp_directory': 'pg_stat_tmp',
            'superuser_reserved_connections': 3,
            'synchronize_seqscans': True,
            'synchronous_commit': True,
            'synchronous_standby_names': None,
            'syslog_facility': 'local0',
            'syslog_ident': 'postgres',
            'tcp_keepalives_count': 0,
            'tcp_keepalives_idle': 0,
            'tcp_keepalives_interval': 0,
            'temp_buffers': 1024,
            'temp_file_limit': -1,
            'temp_tablespaces': None,
            'timezone': 'GB',
            'timezone_abbreviations': 'Default',
            'trace_notify': False,
            'trace_recovery_messages': 'log',
            'trace_sort': False,
            'track_activities': True,
            'track_activity_query_size': 1024,
            'track_counts': True,
            'track_functions': 'none',
            'track_io_timing': False,
            'transaction_deferrable': False,
            'transaction_isolation': 'read committed',
            'transaction_read_only': False,
            'transform_null_equals': False,
            'unix_socket_directories': '/tmp',
            'unix_socket_group': None,
            'unix_socket_permissions': 777,
            'update_process_title': True,
            'vacuum_cost_delay': 0,
            'vacuum_cost_limit': 200,
            'vacuum_cost_page_dirty': 20,
            'vacuum_cost_page_hit': 1,
            'vacuum_cost_page_miss': 10,
            'vacuum_defer_cleanup_age': 0,
            'vacuum_freeze_min_age': 50000000,
            'vacuum_freeze_table_age': 150000000,
            'vacuum_multixact_freeze_min_age': 5000000,
            'vacuum_multixact_freeze_table_age': 150000000,
            'wal_block_size': 8192,
            'wal_buffers': 512,
            'wal_keep_segments': 0,
            'wal_level': 'minimal',
            'wal_log_hints': False,
            'wal_receiver_status_interval': 10,
            'wal_receiver_timeout': 60000,
            'wal_segment_size': 2048,
            'wal_sender_timeout': 60000,
            'wal_sync_method': 'open_datasync',
            'wal_writer_delay': 200,
            'work_mem': 4096,
            'xmlbinary': 'base64',
            'xmloption': 'content',
            'zero_damaged_pages': False}
    
    def test_command_tool(self):
        assert (Postgresql.command_tool(5432, {}, 'SHOW ALL') ==
            ['psql', '--host', '127.0.0.1', '--port', 5432,
                '--dbname', 'template1',
                '--command', 'SHOW ALL',
                '--no-password', '--quiet', '--no-align', '--pset=footer=off'])
    
    def test_command_tool_user(self):
        assert (Postgresql.command_tool(5432, { 'user': "USER" }, 'SHOW ALL') ==
            ['psql', '--host', '127.0.0.1', '--port', 5432,
                '--dbname', 'template1',
                '--command', 'SHOW ALL',
                '--no-password', '--quiet', '--no-align', '--pset=footer=off',
                '--username=USER'])
    
    def test_enabled(self):
        postgresql = Postgresql({}, { 5432: {} })
        
        assert postgresql.enabled() == True
    
    def test_enabled_no_ports(self):
        postgresql = Postgresql({}, {})
        
        assert postgresql.enabled() == False
    
    def test_collect(self, monkeypatch):
        monkeypatch.setattr(BasePortCommand, 'exec_command',
            self.mock_exec_command)
        
        postgresql = Postgresql({}, { 5432: {} })
        metrics = postgresql.collect()
        
        metrics_t = {
            'status':           self.mock_collect_status(),
            'stat_replication': self.mock_collect_stat_replication(),
            'settings':         self.mock_collect_settings()}
        
        assert metrics[5432] == metrics_t
        
        for setting in Postgresql.COLLECT_SETTING_DEFAULTS.keys():
            postgresql2 = Postgresql({}, { 5432: {
                'collect': { setting: False } } })
            metrics2 = postgresql2.collect()
            
            metrics_t2 = metrics_t.copy()
            del metrics_t2[setting]
            assert metrics2[5432] == metrics_t2
