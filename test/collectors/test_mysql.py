import os

from pikka_bird_collector.collectors.mysql import Mysql
from pikka_bird_collector.collectors.base_port_command import BasePortCommand


class TestMysql:
    
    @staticmethod
    def fixture_path(filename):
        return os.path.join(os.path.dirname(__file__), '../fixtures', filename)
    
    @staticmethod
    def read_fixture(filename):
        with open(filename, 'r') as f_h:
            d = f_h.read()
        return d
    
    def mock_cmd_show_status(self):
        f = TestMysql.fixture_path('mysql/show_status.txt')
        return TestMysql.read_fixture(f)
    
    def mock_cmd_show_variables(self):
        f = TestMysql.fixture_path('mysql/show_variables.txt')
        return TestMysql.read_fixture(f)
    
    def mock_exec_command(self, command_f):
        if Mysql.CMD_SHOW_STATUS in command_f:
            return self.mock_cmd_show_status()
        elif Mysql.CMD_SHOW_VARIABLES in command_f:
            return self.mock_cmd_show_variables()
    
    def mock_collect_status(self):
        return {
            'aborted_clients': 0,
            'aborted_connects': 13,
            'binlog_cache_disk_use': 0,
            'binlog_cache_use': 0,
            'binlog_stmt_cache_disk_use': 0,
            'binlog_stmt_cache_use': 0,
            'bytes_received': 224,
            'bytes_sent': 168,
            'com_admin_commands': 0,
            'com_alter_db': 0,
            'com_alter_db_upgrade': 0,
            'com_alter_event': 0,
            'com_alter_function': 0,
            'com_alter_procedure': 0,
            'com_alter_server': 0,
            'com_alter_table': 0,
            'com_alter_tablespace': 0,
            'com_alter_user': 0,
            'com_analyze': 0,
            'com_assign_to_keycache': 0,
            'com_begin': 0,
            'com_binlog': 0,
            'com_call_procedure': 0,
            'com_change_db': 0,
            'com_change_master': 0,
            'com_check': 0,
            'com_checksum': 0,
            'com_commit': 0,
            'com_create_db': 0,
            'com_create_event': 0,
            'com_create_function': 0,
            'com_create_index': 0,
            'com_create_procedure': 0,
            'com_create_server': 0,
            'com_create_table': 0,
            'com_create_trigger': 0,
            'com_create_udf': 0,
            'com_create_user': 0,
            'com_create_view': 0,
            'com_dealloc_sql': 0,
            'com_delete': 0,
            'com_delete_multi': 0,
            'com_do': 0,
            'com_drop_db': 0,
            'com_drop_event': 0,
            'com_drop_function': 0,
            'com_drop_index': 0,
            'com_drop_procedure': 0,
            'com_drop_server': 0,
            'com_drop_table': 0,
            'com_drop_trigger': 0,
            'com_drop_user': 0,
            'com_drop_view': 0,
            'com_empty_query': 0,
            'com_execute_sql': 0,
            'com_flush': 0,
            'com_get_diagnostics': 0,
            'com_grant': 0,
            'com_ha_close': 0,
            'com_ha_open': 0,
            'com_ha_read': 0,
            'com_help': 0,
            'com_insert': 0,
            'com_insert_select': 0,
            'com_install_plugin': 0,
            'com_kill': 0,
            'com_load': 0,
            'com_lock_tables': 0,
            'com_optimize': 0,
            'com_preload_keys': 0,
            'com_prepare_sql': 0,
            'com_purge': 0,
            'com_purge_before_date': 0,
            'com_release_savepoint': 0,
            'com_rename_table': 0,
            'com_rename_user': 0,
            'com_repair': 0,
            'com_replace': 0,
            'com_replace_select': 0,
            'com_reset': 0,
            'com_resignal': 0,
            'com_revoke': 0,
            'com_revoke_all': 0,
            'com_rollback': 0,
            'com_rollback_to_savepoint': 0,
            'com_savepoint': 0,
            'com_select': 1,
            'com_set_option': 0,
            'com_show_binlog_events': 0,
            'com_show_binlogs': 0,
            'com_show_charsets': 0,
            'com_show_collations': 0,
            'com_show_create_db': 0,
            'com_show_create_event': 0,
            'com_show_create_func': 0,
            'com_show_create_proc': 0,
            'com_show_create_table': 0,
            'com_show_create_trigger': 0,
            'com_show_databases': 0,
            'com_show_engine_logs': 0,
            'com_show_engine_mutex': 0,
            'com_show_engine_status': 0,
            'com_show_errors': 0,
            'com_show_events': 0,
            'com_show_fields': 0,
            'com_show_function_code': 0,
            'com_show_function_status': 0,
            'com_show_grants': 0,
            'com_show_keys': 0,
            'com_show_master_status': 0,
            'com_show_open_tables': 0,
            'com_show_plugins': 0,
            'com_show_privileges': 0,
            'com_show_procedure_code': 0,
            'com_show_procedure_status': 0,
            'com_show_processlist': 0,
            'com_show_profile': 0,
            'com_show_profiles': 0,
            'com_show_relaylog_events': 0,
            'com_show_slave_hosts': 0,
            'com_show_slave_status': 0,
            'com_show_status': 1,
            'com_show_storage_engines': 0,
            'com_show_table_status': 0,
            'com_show_tables': 0,
            'com_show_triggers': 0,
            'com_show_variables': 0,
            'com_show_warnings': 0,
            'com_signal': 0,
            'com_slave_start': 0,
            'com_slave_stop': 0,
            'com_stmt_close': 0,
            'com_stmt_execute': 0,
            'com_stmt_fetch': 0,
            'com_stmt_prepare': 0,
            'com_stmt_reprepare': 0,
            'com_stmt_reset': 0,
            'com_stmt_send_long_data': 0,
            'com_truncate': 0,
            'com_uninstall_plugin': 0,
            'com_unlock_tables': 0,
            'com_update': 0,
            'com_update_multi': 0,
            'com_xa_commit': 0,
            'com_xa_end': 0,
            'com_xa_prepare': 0,
            'com_xa_recover': 0,
            'com_xa_rollback': 0,
            'com_xa_start': 0,
            'compression': False,
            'connection_errors_accept': 0,
            'connection_errors_internal': 0,
            'connection_errors_max_connections': 0,
            'connection_errors_peer_address': 0,
            'connection_errors_select': 0,
            'connection_errors_tcpwrap': 0,
            'connections': 148,
            'created_tmp_disk_tables': 0,
            'created_tmp_files': 5,
            'created_tmp_tables': 0,
            'delayed_errors': 0,
            'delayed_insert_threads': 0,
            'delayed_writes': 0,
            'flush_commands': 1,
            'handler_commit': 0,
            'handler_delete': 0,
            'handler_discover': 0,
            'handler_external_lock': 0,
            'handler_mrr_init': 0,
            'handler_prepare': 0,
            'handler_read_first': 0,
            'handler_read_key': 0,
            'handler_read_last': 0,
            'handler_read_next': 0,
            'handler_read_prev': 0,
            'handler_read_rnd': 0,
            'handler_read_rnd_next': 0,
            'handler_rollback': 0,
            'handler_savepoint': 0,
            'handler_savepoint_rollback': 0,
            'handler_update': 0,
            'handler_write': 0,
            'innodb_available_undo_logs': 128,
            'innodb_buffer_pool_bytes_data': 7454720,
            'innodb_buffer_pool_bytes_dirty': 0,
            'innodb_buffer_pool_dump_status': 'not started',
            'innodb_buffer_pool_load_status': 'not started',
            'innodb_buffer_pool_pages_data': 455,
            'innodb_buffer_pool_pages_dirty': 0,
            'innodb_buffer_pool_pages_flushed': 1,
            'innodb_buffer_pool_pages_free': 7736,
            'innodb_buffer_pool_pages_misc': 0,
            'innodb_buffer_pool_pages_total': 8191,
            'innodb_buffer_pool_read_ahead': 0,
            'innodb_buffer_pool_read_ahead_evicted': 0,
            'innodb_buffer_pool_read_ahead_rnd': 0,
            'innodb_buffer_pool_read_requests': 8252,
            'innodb_buffer_pool_reads': 456,
            'innodb_buffer_pool_wait_free': 0,
            'innodb_buffer_pool_write_requests': 1,
            'innodb_data_fsyncs': 5,
            'innodb_data_pending_fsyncs': 0,
            'innodb_data_pending_reads': 0,
            'innodb_data_pending_writes': 0,
            'innodb_data_read': 7540736,
            'innodb_data_reads': 477,
            'innodb_data_writes': 5,
            'innodb_data_written': 34304,
            'innodb_dblwr_pages_written': 1,
            'innodb_dblwr_writes': 1,
            'innodb_have_atomic_builtins': True,
            'innodb_log_waits': 0,
            'innodb_log_write_requests': 0,
            'innodb_log_writes': 1,
            'innodb_num_open_files': 14,
            'innodb_os_log_fsyncs': 3,
            'innodb_os_log_pending_fsyncs': 0,
            'innodb_os_log_pending_writes': 0,
            'innodb_os_log_written': 512,
            'innodb_page_size': 16384,
            'innodb_pages_created': 0,
            'innodb_pages_read': 455,
            'innodb_pages_written': 1,
            'innodb_row_lock_current_waits': 0,
            'innodb_row_lock_time': 0,
            'innodb_row_lock_time_avg': 0,
            'innodb_row_lock_time_max': 0,
            'innodb_row_lock_waits': 0,
            'innodb_rows_deleted': 0,
            'innodb_rows_inserted': 0,
            'innodb_rows_read': 0,
            'innodb_rows_updated': 0,
            'innodb_truncated_status_writes': 0,
            'key_blocks_not_flushed': 0,
            'key_blocks_unused': 6698,
            'key_blocks_used': 0,
            'key_read_requests': 0,
            'key_reads': 0,
            'key_write_requests': 0,
            'key_writes': 0,
            'last_query_cost': 0.0,
            'last_query_partial_plans': 0,
            'max_used_connections': 2,
            'not_flushed_delayed_rows': 0,
            'open_files': 18,
            'open_streams': 0,
            'open_table_definitions': 68,
            'open_tables': 61,
            'opened_files': 118,
            'opened_table_definitions': 0,
            'opened_tables': 0,
            'performance_schema_accounts_lost': 0,
            'performance_schema_cond_classes_lost': 0,
            'performance_schema_cond_instances_lost': 0,
            'performance_schema_digest_lost': 0,
            'performance_schema_file_classes_lost': 0,
            'performance_schema_file_handles_lost': 0,
            'performance_schema_file_instances_lost': 0,
            'performance_schema_hosts_lost': 0,
            'performance_schema_locker_lost': 0,
            'performance_schema_mutex_classes_lost': 0,
            'performance_schema_mutex_instances_lost': 0,
            'performance_schema_rwlock_classes_lost': 0,
            'performance_schema_rwlock_instances_lost': 0,
            'performance_schema_session_connect_attrs_lost': 0,
            'performance_schema_socket_classes_lost': 0,
            'performance_schema_socket_instances_lost': 0,
            'performance_schema_stage_classes_lost': 0,
            'performance_schema_statement_classes_lost': 0,
            'performance_schema_table_handles_lost': 0,
            'performance_schema_table_instances_lost': 0,
            'performance_schema_thread_classes_lost': 0,
            'performance_schema_thread_instances_lost': 0,
            'performance_schema_users_lost': 0,
            'prepared_stmt_count': 0,
            'qcache_free_blocks': 1,
            'qcache_free_memory': 1031336,
            'qcache_hits': 0,
            'qcache_inserts': 0,
            'qcache_lowmem_prunes': 0,
            'qcache_not_cached': 136,
            'qcache_queries_in_cache': 0,
            'qcache_total_blocks': 1,
            'queries': 410,
            'questions': 2,
            'rsa_public_key': None,
            'select_full_join': 0,
            'select_full_range_join': 0,
            'select_range': 0,
            'select_range_check': 0,
            'select_scan': 0,
            'slave_heartbeat_period': None,
            'slave_last_heartbeat': None,
            'slave_open_temp_tables': 0,
            'slave_received_heartbeats': None,
            'slave_retried_transactions': None,
            'slave_running': False,
            'slow_launch_threads': 0,
            'slow_queries': 0,
            'sort_merge_passes': 0,
            'sort_range': 0,
            'sort_rows': 0,
            'sort_scan': 0,
            'ssl_accept_renegotiates': 0,
            'ssl_accepts': 0,
            'ssl_callback_cache_hits': 0,
            'ssl_cipher': None,
            'ssl_cipher_list': None,
            'ssl_client_connects': 0,
            'ssl_connect_renegotiates': 0,
            'ssl_ctx_verify_depth': 0,
            'ssl_ctx_verify_mode': 0,
            'ssl_default_timeout': 0,
            'ssl_finished_accepts': 0,
            'ssl_finished_connects': 0,
            'ssl_server_not_after': None,
            'ssl_server_not_before': None,
            'ssl_session_cache_hits': 0,
            'ssl_session_cache_misses': 0,
            'ssl_session_cache_mode': 'NONE',
            'ssl_session_cache_overflows': 0,
            'ssl_session_cache_size': 0,
            'ssl_session_cache_timeouts': 0,
            'ssl_sessions_reused': 0,
            'ssl_used_session_cache_entries': 0,
            'ssl_verify_depth': 0,
            'ssl_verify_mode': 0,
            'ssl_version': None,
            'table_locks_immediate': 74,
            'table_locks_waited': 0,
            'table_open_cache_hits': 0,
            'table_open_cache_misses': 0,
            'table_open_cache_overflows': 0,
            'tc_log_max_pages_used': 0,
            'tc_log_page_size': 0,
            'tc_log_page_waits': 0,
            'threads_cached': 0,
            'threads_connected': 2,
            'threads_created': 2,
            'threads_running': 1,
            'uptime': 2616535,
            'uptime_since_flush_status': 2616535}
    
    def mock_collect_variables(self):
        return {
            'auto_increment_increment': 1,
            'auto_increment_offset': 1,
            'autocommit': True,
            'automatic_sp_privileges': True,
            'back_log': 80,
            'basedir': '/usr/local/Cellar/mysql/5.6.23',
            'big_tables': False,
            'bind_address': '127.0.0.1',
            'binlog_cache_size': 32768,
            'binlog_checksum': 'CRC32',
            'binlog_direct_non_transactional_updates': False,
            'binlog_error_action': 'IGNORE_ERROR',
            'binlog_format': 'STATEMENT',
            'binlog_gtid_simple_recovery': False,
            'binlog_max_flush_queue_time': 0,
            'binlog_order_commits': True,
            'binlog_row_image': 'FULL',
            'binlog_rows_query_log_events': False,
            'binlog_stmt_cache_size': 32768,
            'binlogging_impossible_mode': 'IGNORE_ERROR',
            'block_encryption_mode': 'aes-128-ecb',
            'bulk_insert_buffer_size': 8388608,
            'character_set_client': 'utf8',
            'character_set_connection': 'utf8',
            'character_set_database': 'utf8',
            'character_set_filesystem': 'binary',
            'character_set_results': 'utf8',
            'character_set_server': 'utf8',
            'character_set_system': 'utf8',
            'character_sets_dir': '/usr/local/Cellar/mysql/5.6.23/share/mysql/charsets/',
            'collation_connection': 'utf8_general_ci',
            'collation_database': 'utf8_general_ci',
            'collation_server': 'utf8_general_ci',
            'completion_type': 'NO_CHAIN',
            'concurrent_insert': 'AUTO',
            'connect_timeout': 10,
            'core_file': False,
            'datadir': '/usr/local/var/mysql/',
            'date_format': '%Y-%m-%d',
            'datetime_format': '%Y-%m-%d %H:%i:%s',
            'default_storage_engine': 'InnoDB',
            'default_tmp_storage_engine': 'InnoDB',
            'default_week_format': 0,
            'delay_key_write': True,
            'delayed_insert_limit': 100,
            'delayed_insert_timeout': 300,
            'delayed_queue_size': 1000,
            'disconnect_on_expired_password': True,
            'div_precision_increment': 4,
            'end_markers_in_json': False,
            'enforce_gtid_consistency': False,
            'eq_range_index_dive_limit': 10,
            'error_count': 0,
            'event_scheduler': False,
            'expire_logs_days': 0,
            'explicit_defaults_for_timestamp': False,
            'external_user': None,
            'flush': False,
            'flush_time': 0,
            'foreign_key_checks': True,
            'ft_boolean_syntax': '+ -><()~*:""&|',
            'ft_max_word_len': 84,
            'ft_min_word_len': 4,
            'ft_query_expansion_limit': 20,
            'ft_stopword_file': '(built-in)',
            'general_log': False,
            'general_log_file': '/usr/local/var/mysql/tiredpixel.log',
            'group_concat_max_len': 1024,
            'gtid_executed': None,
            'gtid_mode': False,
            'gtid_next': 'AUTOMATIC',
            'gtid_owned': None,
            'gtid_purged': None,
            'have_compress': True,
            'have_crypt': True,
            'have_dynamic_loading': True,
            'have_geometry': True,
            'have_openssl': 'DISABLED',
            'have_profiling': True,
            'have_query_cache': True,
            'have_rtree_keys': True,
            'have_ssl': 'DISABLED',
            'have_symlink': True,
            'host_cache_size': 279,
            'hostname': 'tiredpixel.home',
            'identity': 0,
            'ignore_builtin_innodb': False,
            'ignore_db_dirs': None,
            'init_connect': None,
            'init_file': None,
            'init_slave': None,
            'innodb_adaptive_flushing': True,
            'innodb_adaptive_flushing_lwm': 10,
            'innodb_adaptive_hash_index': True,
            'innodb_adaptive_max_sleep_delay': 150000,
            'innodb_additional_mem_pool_size': 8388608,
            'innodb_api_bk_commit_interval': 5,
            'innodb_api_disable_rowlock': False,
            'innodb_api_enable_binlog': False,
            'innodb_api_enable_mdl': False,
            'innodb_api_trx_level': 0,
            'innodb_autoextend_increment': 64,
            'innodb_autoinc_lock_mode': 1,
            'innodb_buffer_pool_dump_at_shutdown': False,
            'innodb_buffer_pool_dump_now': False,
            'innodb_buffer_pool_filename': 'ib_buffer_pool',
            'innodb_buffer_pool_instances': 8,
            'innodb_buffer_pool_load_abort': False,
            'innodb_buffer_pool_load_at_startup': False,
            'innodb_buffer_pool_load_now': False,
            'innodb_buffer_pool_size': 134217728,
            'innodb_change_buffer_max_size': 25,
            'innodb_change_buffering': 'all',
            'innodb_checksum_algorithm': 'innodb',
            'innodb_checksums': True,
            'innodb_cmp_per_index_enabled': False,
            'innodb_commit_concurrency': 0,
            'innodb_compression_failure_threshold_pct': 5,
            'innodb_compression_level': 6,
            'innodb_compression_pad_pct_max': 50,
            'innodb_concurrency_tickets': 5000,
            'innodb_data_file_path': 'ibdata1:12M:autoextend',
            'innodb_data_home_dir': None,
            'innodb_disable_sort_file_cache': False,
            'innodb_doublewrite': True,
            'innodb_fast_shutdown': 1,
            'innodb_file_format': 'Antelope',
            'innodb_file_format_check': True,
            'innodb_file_format_max': 'Antelope',
            'innodb_file_per_table': True,
            'innodb_flush_log_at_timeout': 1,
            'innodb_flush_log_at_trx_commit': 1,
            'innodb_flush_method': None,
            'innodb_flush_neighbors': 1,
            'innodb_flushing_avg_loops': 30,
            'innodb_force_load_corrupted': False,
            'innodb_force_recovery': 0,
            'innodb_ft_aux_table': None,
            'innodb_ft_cache_size': 8000000,
            'innodb_ft_enable_diag_print': False,
            'innodb_ft_enable_stopword': True,
            'innodb_ft_max_token_size': 84,
            'innodb_ft_min_token_size': 3,
            'innodb_ft_num_word_optimize': 2000,
            'innodb_ft_result_cache_limit': 2000000000,
            'innodb_ft_server_stopword_table': None,
            'innodb_ft_sort_pll_degree': 2,
            'innodb_ft_total_cache_size': 640000000,
            'innodb_ft_user_stopword_table': None,
            'innodb_io_capacity': 200,
            'innodb_io_capacity_max': 2000,
            'innodb_large_prefix': False,
            'innodb_lock_wait_timeout': 50,
            'innodb_locks_unsafe_for_binlog': False,
            'innodb_log_buffer_size': 8388608,
            'innodb_log_compressed_pages': True,
            'innodb_log_file_size': 50331648,
            'innodb_log_files_in_group': 2,
            'innodb_log_group_home_dir': './',
            'innodb_lru_scan_depth': 1024,
            'innodb_max_dirty_pages_pct': 75,
            'innodb_max_dirty_pages_pct_lwm': 0,
            'innodb_max_purge_lag': 0,
            'innodb_max_purge_lag_delay': 0,
            'innodb_mirrored_log_groups': 1,
            'innodb_monitor_disable': None,
            'innodb_monitor_enable': None,
            'innodb_monitor_reset': None,
            'innodb_monitor_reset_all': None,
            'innodb_old_blocks_pct': 37,
            'innodb_old_blocks_time': 1000,
            'innodb_online_alter_log_max_size': 134217728,
            'innodb_open_files': 2000,
            'innodb_optimize_fulltext_only': False,
            'innodb_page_size': 16384,
            'innodb_print_all_deadlocks': False,
            'innodb_purge_batch_size': 300,
            'innodb_purge_threads': 1,
            'innodb_random_read_ahead': False,
            'innodb_read_ahead_threshold': 56,
            'innodb_read_io_threads': 4,
            'innodb_read_only': False,
            'innodb_replication_delay': 0,
            'innodb_rollback_on_timeout': False,
            'innodb_rollback_segments': 128,
            'innodb_sort_buffer_size': 1048576,
            'innodb_spin_wait_delay': 6,
            'innodb_stats_auto_recalc': True,
            'innodb_stats_method': 'nulls_equal',
            'innodb_stats_on_metadata': False,
            'innodb_stats_persistent': True,
            'innodb_stats_persistent_sample_pages': 20,
            'innodb_stats_sample_pages': 8,
            'innodb_stats_transient_sample_pages': 8,
            'innodb_status_output': False,
            'innodb_status_output_locks': False,
            'innodb_strict_mode': False,
            'innodb_support_xa': True,
            'innodb_sync_array_size': 1,
            'innodb_sync_spin_loops': 30,
            'innodb_table_locks': True,
            'innodb_thread_concurrency': 0,
            'innodb_thread_sleep_delay': 10000,
            'innodb_undo_directory': '.',
            'innodb_undo_logs': 128,
            'innodb_undo_tablespaces': 0,
            'innodb_use_native_aio': False,
            'innodb_use_sys_malloc': True,
            'innodb_version': '5.6.23',
            'innodb_write_io_threads': 4,
            'insert_id': 0,
            'interactive_timeout': 28800,
            'join_buffer_size': 262144,
            'keep_files_on_create': False,
            'key_buffer_size': 8388608,
            'key_cache_age_threshold': 300,
            'key_cache_block_size': 1024,
            'key_cache_division_limit': 100,
            'large_files_support': True,
            'large_page_size': 0,
            'large_pages': False,
            'last_insert_id': 0,
            'lc_messages': 'en_US',
            'lc_messages_dir': '/usr/local/Cellar/mysql/5.6.23/share/mysql/',
            'lc_time_names': 'en_US',
            'license': 'GPL',
            'local_infile': True,
            'lock_wait_timeout': 31536000,
            'locked_in_memory': False,
            'log_bin': False,
            'log_bin_basename': None,
            'log_bin_index': None,
            'log_bin_trust_function_creators': False,
            'log_bin_use_v1_row_events': False,
            'log_error': '/usr/local/var/mysql/tiredpixel.home.err',
            'log_output': 'FILE',
            'log_queries_not_using_indexes': False,
            'log_slave_updates': False,
            'log_slow_admin_statements': False,
            'log_slow_slave_statements': False,
            'log_throttle_queries_not_using_indexes': 0,
            'log_warnings': 1,
            'long_query_time': 10.000000,
            'low_priority_updates': False,
            'lower_case_file_system': True,
            'lower_case_table_names': 2,
            'master_info_repository': 'FILE',
            'master_verify_checksum': False,
            'max_allowed_packet': 4194304,
            'max_binlog_cache_size': 18446744073709547520,
            'max_binlog_size': 1073741824,
            'max_binlog_stmt_cache_size': 18446744073709547520,
            'max_connect_errors': 100,
            'max_connections': 151,
            'max_delayed_threads': 20,
            'max_error_count': 64,
            'max_heap_table_size': 16777216,
            'max_insert_delayed_threads': 20,
            'max_join_size': 18446744073709551615,
            'max_length_for_sort_data': 1024,
            'max_prepared_stmt_count': 16382,
            'max_relay_log_size': 0,
            'max_seeks_for_key': 18446744073709551615,
            'max_sort_length': 1024,
            'max_sp_recursion_depth': 0,
            'max_tmp_tables': 32,
            'max_user_connections': 0,
            'max_write_lock_count': 18446744073709551615,
            'metadata_locks_cache_size': 1024,
            'metadata_locks_hash_instances': 8,
            'min_examined_row_limit': 0,
            'multi_range_count': 256,
            'myisam_data_pointer_size': 6,
            'myisam_max_sort_file_size': 9223372036853727232,
            'myisam_mmap_size': 18446744073709551615,
            'myisam_recover_options': False,
            'myisam_repair_threads': 1,
            'myisam_sort_buffer_size': 8388608,
            'myisam_stats_method': 'nulls_unequal',
            'myisam_use_mmap': False,
            'net_buffer_length': 16384,
            'net_read_timeout': 30,
            'net_retry_count': 10,
            'net_write_timeout': 60,
            'new': False,
            'old': False,
            'old_alter_table': False,
            'old_passwords': 0,
            'open_files_limit': 5000,
            'optimizer_prune_level': 1,
            'optimizer_search_depth': 62,
            'optimizer_switch': 'index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,subquery_materialization_cost_based=on,use_index_extensions=on',
            'optimizer_trace': 'enabled=off,one_line=off',
            'optimizer_trace_features': 'greedy_search=on,range_optimizer=on,dynamic_range=on,repeated_subselect=on',
            'optimizer_trace_limit': 1,
            'optimizer_trace_max_mem_size': 16384,
            'optimizer_trace_offset': -1,
            'performance_schema': True,
            'performance_schema_accounts_size': 100,
            'performance_schema_digests_size': 10000,
            'performance_schema_events_stages_history_long_size': 10000,
            'performance_schema_events_stages_history_size': 10,
            'performance_schema_events_statements_history_long_size': 10000,
            'performance_schema_events_statements_history_size': 10,
            'performance_schema_events_waits_history_long_size': 10000,
            'performance_schema_events_waits_history_size': 10,
            'performance_schema_hosts_size': 100,
            'performance_schema_max_cond_classes': 80,
            'performance_schema_max_cond_instances': 3504,
            'performance_schema_max_file_classes': 50,
            'performance_schema_max_file_handles': 32768,
            'performance_schema_max_file_instances': 7693,
            'performance_schema_max_mutex_classes': 200,
            'performance_schema_max_mutex_instances': 15906,
            'performance_schema_max_rwlock_classes': 40,
            'performance_schema_max_rwlock_instances': 9102,
            'performance_schema_max_socket_classes': 10,
            'performance_schema_max_socket_instances': 322,
            'performance_schema_max_stage_classes': 150,
            'performance_schema_max_statement_classes': 168,
            'performance_schema_max_table_handles': 4000,
            'performance_schema_max_table_instances': 12500,
            'performance_schema_max_thread_classes': 50,
            'performance_schema_max_thread_instances': 402,
            'performance_schema_session_connect_attrs_size': 512,
            'performance_schema_setup_actors_size': 100,
            'performance_schema_setup_objects_size': 100,
            'performance_schema_users_size': 100,
            'pid_file': '/usr/local/var/mysql/tiredpixel.home.pid',
            'plugin_dir': '/usr/local/Cellar/mysql/5.6.23/lib/plugin/',
            'port': 3306,
            'preload_buffer_size': 32768,
            'profiling': False,
            'profiling_history_size': 15,
            'protocol_version': 10,
            'proxy_user': None,
            'pseudo_slave_mode': False,
            'pseudo_thread_id': 80,
            'query_alloc_block_size': 8192,
            'query_cache_limit': 1048576,
            'query_cache_min_res_unit': 4096,
            'query_cache_size': 1048576,
            'query_cache_type': False,
            'query_cache_wlock_invalidate': False,
            'query_prealloc_size': 8192,
            'rand_seed1': 0,
            'rand_seed2': 0,
            'range_alloc_block_size': 4096,
            'read_buffer_size': 131072,
            'read_only': False,
            'read_rnd_buffer_size': 262144,
            'relay_log': None,
            'relay_log_basename': None,
            'relay_log_index': None,
            'relay_log_info_file': 'relay-log.info',
            'relay_log_info_repository': 'FILE',
            'relay_log_purge': True,
            'relay_log_recovery': False,
            'relay_log_space_limit': 0,
            'report_host': None,
            'report_password': None,
            'report_port': 3306,
            'report_user': None,
            'rpl_stop_slave_timeout': 31536000,
            'secure_auth': True,
            'secure_file_priv': None,
            'server_id': 0,
            'server_id_bits': 32,
            'server_uuid': '5d2f94a0-4658-11e4-92e7-0a41270292d6',
            'sha256_password_private_key_path': 'private_key.pem',
            'sha256_password_public_key_path': 'public_key.pem',
            'simplified_binlog_gtid_recovery': False,
            'skip_external_locking': True,
            'skip_name_resolve': False,
            'skip_networking': False,
            'skip_show_database': False,
            'slave_allow_batching': False,
            'slave_checkpoint_group': 512,
            'slave_checkpoint_period': 300,
            'slave_compressed_protocol': False,
            'slave_exec_mode': 'STRICT',
            'slave_load_tmpdir': '/var/folders/wl/9pmj8jnd33d8pgrn9gd1gl5r0000gn/T/',
            'slave_max_allowed_packet': 1073741824,
            'slave_net_timeout': 3600,
            'slave_parallel_workers': 0,
            'slave_pending_jobs_size_max': 16777216,
            'slave_rows_search_algorithms': 'TABLE_SCAN,INDEX_SCAN',
            'slave_skip_errors': False,
            'slave_sql_verify_checksum': True,
            'slave_transaction_retries': 10,
            'slave_type_conversions': None,
            'slow_launch_time': 2,
            'slow_query_log': False,
            'slow_query_log_file': '/usr/local/var/mysql/tiredpixel-slow.log',
            'socket': '/tmp/mysql.sock',
            'sort_buffer_size': 262144,
            'sql_auto_is_null': False,
            'sql_big_selects': True,
            'sql_buffer_result': False,
            'sql_log_bin': True,
            'sql_log_off': False,
            'sql_mode': 'NO_ENGINE_SUBSTITUTION',
            'sql_notes': True,
            'sql_quote_show_create': True,
            'sql_safe_updates': False,
            'sql_select_limit': 18446744073709551615,
            'sql_slave_skip_counter': 0,
            'sql_warnings': False,
            'ssl_ca': None,
            'ssl_capath': None,
            'ssl_cert': None,
            'ssl_cipher': None,
            'ssl_crl': None,
            'ssl_crlpath': None,
            'ssl_key': None,
            'storage_engine': 'InnoDB',
            'stored_program_cache': 256,
            'sync_binlog': 0,
            'sync_frm': True,
            'sync_master_info': 10000,
            'sync_relay_log': 10000,
            'sync_relay_log_info': 10000,
            'system_time_zone': 'BST',
            'table_definition_cache': 1400,
            'table_open_cache': 2000,
            'table_open_cache_instances': 1,
            'thread_cache_size': 9,
            'thread_concurrency': 10,
            'thread_handling': 'one-thread-per-connection',
            'thread_stack': 262144,
            'time_format': '%H:%i:%s',
            'time_zone': 'SYSTEM',
            'timed_mutexes': False,
            'timestamp': 1430653686.849428,
            'tmp_table_size': 16777216,
            'tmpdir': '/var/folders/wl/9pmj8jnd33d8pgrn9gd1gl5r0000gn/T/',
            'transaction_alloc_block_size': 8192,
            'transaction_allow_batching': False,
            'transaction_prealloc_size': 4096,
            'tx_isolation': 'REPEATABLE-READ',
            'tx_read_only': False,
            'unique_checks': True,
            'updatable_views_with_limit': True,
            'version': '5.6.23',
            'version_comment': 'Homebrew',
            'version_compile_machine': 'x86_64',
            'version_compile_os': 'osx10.10',
            'wait_timeout': 28800,
            'warning_count': 0}
    
    def test_command_tool(self):
        assert (Mysql.command_tool(3306, {}, 'SHOW VARIABLES') ==
            ['mysql', '--host', '127.0.0.1', '--port', 3306,
                '--execute', 'SHOW VARIABLES',
                '--batch', '--raw', '--skip-column-names'])
    
    def test_command_tool_user(self):
        assert (Mysql.command_tool(3306, { 'user': "USER" }, 'SHOW VARIABLES') ==
            ['mysql', '--host', '127.0.0.1', '--port', 3306,
                '--execute', 'SHOW VARIABLES',
                '--batch', '--raw', '--skip-column-names',
                '--user=USER'])
    
    def test_command_tool_password(self):
        assert (Mysql.command_tool(3306, { 'password': 'PASS"WORD' }, 'SHOW VARIABLES') ==
            ['mysql', '--host', '127.0.0.1', '--port', 3306,
                '--execute', 'SHOW VARIABLES',
                '--batch', '--raw', '--skip-column-names',
                '--password=PASS"WORD'])
    
    def test_parse_output_none(self):
        assert Mysql.parse_output(None) == {}
    
    def test_parse_output_show_variables(self):
        assert Mysql.parse_output(self.mock_cmd_show_variables(),
            convert_bool=True) == self.mock_collect_variables()
    
    def test_parse_output_show_status(self):
        assert Mysql.parse_output(self.mock_cmd_show_status(),
            convert_bool=True) == self.mock_collect_status()
    
    def test_enabled(self):
        mysql = Mysql({}, { 3306: {} })
        
        assert mysql.enabled() == True
    
    def test_enabled_no_ports(self):
        mysql = Mysql({}, {})
        
        assert mysql.enabled() == False
    
    def test_collect(self, monkeypatch):
        monkeypatch.setattr(BasePortCommand, 'exec_command',
            self.mock_exec_command)
        
        mysql = Mysql({}, { 3306: {} })
        metrics = mysql.collect()
        
        assert metrics == {
            3306: {
                'status':    self.mock_collect_status(),
                'variables': self.mock_collect_variables()}}
    
    def test_collect_no_variables(self, monkeypatch):
        monkeypatch.setattr(BasePortCommand, 'exec_command',
            self.mock_exec_command)
        
        mysql = Mysql({}, { 3306: { 'variables': False } })
        metrics = mysql.collect()
        
        assert metrics == {
            3306: {
                'status': self.mock_collect_status()}}
