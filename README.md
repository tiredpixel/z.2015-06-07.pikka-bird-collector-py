# Pikka Bird Collector (Python)

[![PyPI version](https://badge.fury.io/py/pikka-bird-collector.svg)](http://badge.fury.io/py/pikka-bird-collector)
[![Build Status](https://travis-ci.org/tiredpixel/pikka-bird-collector-py.png?branch=master,stable)](https://travis-ci.org/tiredpixel/pikka-bird-collector-py)

Pikka Bird ops monitoring tool Collector component.

Pikka Bird Collector gathers metrics reports, sending them to
[Pikka Bird Server][server]. Pikka Bird Collector is a [Python][python]
application.

Supported collectors include: system, MongoDB, MySQL, PostgreSQL, RabbitMQ, and
Redis. For more details, see below.

Pikka Bird is currently in a draft phase, which means that payloads and schemas
might be changed in a backwards-incompatible fashion. Although it is unlikely,
in extreme cases this could require you to reinstall with an empty database. If
this upsets you too much, please say hello and come back later. :) Currently, it
is not recommended that you use Pikka Bird as a replacement for any of your
usual monitoring tools.

More sleep lost by [tiredpixel](https://www.tiredpixel.com/).


## Installation

Install the following externals:

- [Python][python]
  
  The default version supported is defined in `.python-version`. Any other
  versions supported as defined in `.travis.yml`.

- [Pikka Bird Server][server]
  
  Pikka Bird Server collects the metrics Pikka Bird Collector gathers.

Install using [Pip][pip]:

    pip install pikka-bird-collector

There are currently no released server packages (stay tuned).


## Usage

Run [Pikka Bird Server][server].

To run the collector once:

    pikka-bird-collector

To run the collector eternally, staggering to average once per minute:

    pikka-bird-collector -e 60

To load service confs:

    pikka-bird-collector -c test/fixtures/config/config.json

where the config is something like:

    # config.json

    {
      "redis": {
        "6379": null,
        "6380": {
          "password": "PASSWORD"
        },
        "6381": {}
      }
    }

or maybe something like:

    # config.yaml

    redis:
      6379:
      6380:
        password: "PASSWORD"
      6381: {}

or even a directory of files, e.g. `-c test/fixtures/config/conf.d`

Help is at hand:

    pikka-bird-collector -h


## Collectors

Here follows an overview of each collector supported. Usually, there is nothing
extra to install in order to start monitoring one of these services; merely add
a conf declaration as above, which might need to be no more than just the port.

For more details about each collector, please see the documentation in
`pikka_bird_collector/collectors/`.

### System

Collector for system.

    {'memory': {'swap': {'b': 2147483648, 'sout': {'b': 1213657088}, 'free': {'b': 950534144, '/': 0.44}, 'used': {'b': 1196949504, '/': 0.56}, 'sin': {'b': 66084589568}}, 'virtual': {'inactive': {'b': 968835072, '/': 0.11}, 'avail': {'b': 4248592384, '/': 0.49}, 'unavail': {'b': 4341342208, '/': 0.51}, 'used': {'b': 4688113664, '/': 0.55}, 'buffers': {'b': 258020000, '/': 0.03}, 'b': 8589934592, 'active': {'b': 2415570944, '/': 0.28}, 'cached': {'b': 241716800, '/': 0.03}, 'shared': {'b': 50448000, '/': 0.01}, 'free': {'b': 3279757312, '/': 0.38}, 'wired': {'b': 1303707648, '/': 0.15}}}, 'cpu': {0: {'busy': {'system': {'/': 0.02}, '/': 0.45, 'irq': {'/': 0.05}, 'iowait': {'/': 0.04}, 'softirq': {'/': 0.06}, 'user': {'/': 0.01}, 'nice': {'/': 0.03}, 'guest': {'/': 0.08}, 'guest_nice': {'/': 0.09}, 'steal': {'/': 0.07}}, 'idle': {'/': 0.55}}}, 'load': {'avg': {'15': 126.0, '1': 42.0, '5': 84.0}}, 'disk': {'/': {'flags': 1772, 'space': {'b': 100440011101, 'free': {'b': 98639472987, '/': 0.98}, 'used': {'b': 1800538114, '/': 0.02}}, 'inodes': {'n': 1769, 'avail': {'n': 3111696, '/': 1759.01}, 'free': {'n': 130691232, '/': 73878.59}}, 'block_size': {'b': 1764}, 'device': '/dev/disk42', 'filename_len_max': 1773, 'fragment_size': {'b': 1765}, 'blocks': {'n': 42, 'avail': {'n': 1768, '/': 42.1}, 'free': {'n': 74088, '/': 1764.0}}, 'fstype': 'zaphod'}}}

### MongoDB

Collector for MongoDB (https://www.mongodb.org/).

    {'server_status': {'uptimeEstimate': 22874, 'metrics': {'storage': {'freelist': {'search': {'scanned': 0, 'bucketExhausted': 0, 'requests': 0}}}, 'queryExecutor': {'scanned': 0, 'scannedObjects': 0}, 'cursor': {'open': {'pinned': 0, 'noTimeout': 0, 'total': 0}, 'timedOut': 0}, 'repl': {'buffer': {'sizeBytes': 0, 'maxSizeBytes': 268435456, 'count': 0}, 'apply': {'ops': 0, 'batches': {'num': 0, 'totalMillis': 0}}, 'preload': {'docs': {'num': 0, 'totalMillis': 0}, 'indexes': {'num': 0, 'totalMillis': 0}}, 'network': {'ops': 0, 'getmores': {'num': 0, 'totalMillis': 0}, 'bytes': 0, 'readersCreated': 0}}, 'commands': {'listDatabases': {'failed': 0, 'total': 1}, 'getLog': {'failed': 0, 'total': 8}, 'whatsmyuri': {'failed': 0, 'total': 26}, 'replSetGetStatus': {'failed': 16, 'total': 16}, 'top': {'failed': 0, 'total': 5}, 'ping': {'failed': 0, 'total': 4}, 'getnonce': {'failed': 0, 'total': 2}, 'serverStatus': {'failed': 0, 'total': 15}, 'dbStats': {'failed': 1, 'total': 4}, 'isMaster': {'failed': 0, 'total': 34}, '<UNKNOWN>': 4}, 'document': {'returned': 0, 'updated': 0, 'inserted': 0, 'deleted': 0}, 'ttl': {'deletedDocuments': 0, 'passes': 1883}, 'record': {'moves': 0}, 'getLastError': {'wtimeouts': 0, 'wtime': {'num': 0, 'totalMillis': 0}}, 'operation': {'fastmod': 0, 'scanAndOrder': 0, 'idhack': 0, 'writeConflicts': 0}}, 'asserts': {'warning': 0, 'regular': 0, 'rollovers': 0, 'msg': 0, 'user': 0}, 'host': 'tiredpixel.home', 'backgroundFlushing': {'average_ms': 4.1476367498672335, 'last_finished': '2015-05-16T15:45:53.346Z', 'total_ms': 7810, 'flushes': 1883, 'last_ms': 5}, 'dur': {'journaledMB': 0, 'commitsInWriteLock': 0, 'compression': 0, 'timeMs': {'remapPrivateView': 0, 'commitsInWriteLock': 0, 'prepLogBuffer': 0, 'writeToDataFiles': 0, 'writeToJournal': 0, 'commits': 0, 'dt': 3067}, 'writeToDataFilesMB': 0, 'earlyCommits': 0, 'commits': 10}, 'writeBacksQueued': False, 'network': {'bytesIn': 8422, 'bytesOut': 182467, 'numRequests': 120}, 'mem': {'bits': 64, 'resident': 50, 'virtual': 2973, 'mappedWithJournal': 480, 'mapped': 240, 'supported': True}, 'pid': 286, 'globalLock': {'currentQueue': {'readers': 0, 'writers': 0, 'total': 0}, 'totalTime': '618021658000', 'activeClients': {'readers': 0, 'writers': 0, 'total': 10}}, 'opcountersRepl': {'insert': 0, 'delete': 0, 'getmore': 0, 'update': 0, 'command': 0, 'query': 0}, 'extra_info': {'page_faults': 175428, 'note': 'fields vary by platform'}, 'opcounters': {'insert': 0, 'delete': 0, 'getmore': 0, 'update': 0, 'command': 115, 'query': 2}, 'storageEngine': {'name': 'mmapv1'}, 'connections': {'totalCreated': 28, 'current': 2, 'available': 202}, 'ok': 1, 'cursors': {'clientCursors_size': 0, 'pinned': 0, 'timedOut': 0, 'note': 'deprecated, use server status metrics', 'totalOpen': 0, 'totalNoTimeout': 0}, 'localTime': '2015-05-16T15:46:30.380Z', 'locks': {'Collection': {'acquireCount': {'R': 385078}}, 'Metadata': {'acquireCount': {'R': 1}}, 'MMAPV1Journal': {'timeAcquiringMicros': {'w': 131, 'R': 7163519}, 'acquireWaitCount': {'w': 3, 'R': 4}, 'acquireCount': {'w': 35, 'R': 354821, 'r': 366255}}, 'Database': {'acquireCount': {'R': 6, 'r': 366251, 'W': 15}}, 'Global': {'acquireCount': {'w': 15, 'r': 366257, 'W': 5}}}, 'version': '3.0.2', 'uptimeMillis': 618021690, 'process': 'mongod', 'uptime': 618022}, 'rs_status': {'members': [{'optime': 1404225575, '_id': 0, 'electionDate': '2014-05-01T14:39:46Z', 'state': 1, 'health': 1, 'stateStr': 'PRIMARY', 'name': 'm1.example.net:27017', 'optimeDate': '2014-05-01T14:39:35Z', 'uptime': 269, 'self': True, 'electionTime': 1404225586}, {'lastHeartbeat': '2014-05-01T14:44:03Z', 'optime': 1404225575, 'state': 2, 'pingMs': 0, 'stateStr': 'SECONDARY', 'syncingTo': 'm1.example.net:27017', '_id': 1, 'lastHeartbeatRecv': '2014-05-01T14:44:02Z', 'health': 1, 'name': 'm2.example.net:27017', 'optimeDate': '2014-05-01T14:39:35Z', 'uptime': 265}, {'lastHeartbeat': '2014-05-01T14:44:02Z', 'optime': 1404225575, 'state': 2, 'pingMs': 0, 'stateStr': 'SECONDARY', 'syncingTo': 'm1.example.net:27017', '_id': 2, 'lastHeartbeatRecv': '2014-05-01T14:44:02Z', 'health': 1, 'name': 'm3.example.net:27017', 'optimeDate': '2014-05-01T14:39:35Z', 'uptime': 265}], 'date': '2014-05-01T14:44:03Z', 'set': 'replset', 'ok': 1, 'myState': 1}}

### MySQL

Collector for MySQL (https://www.mysql.com/).

    {'slave_status': {'master_ssl_cert': None, 'until_log_file': None, 'seconds_behind_master': 0, 'relay_log_file': 'mysqld-relay-bin.000064', 'slave_io_state': 'Waiting for master to send event', 'slave_sql_running': True, 'exec_master_log_pos': 64707836, 'master_port': 3306, 'master_user': 'repl', 'last_sql_error': None, 'last_errno': 0, 'master_ssl_key': None, 'relay_master_log_file': 'mysql-bin.000024', 'master_ssl_allowed': False, 'read_master_log_pos': 64707836, 'master_host': 'i-00000000.example.com', 'last_sql_errno': 0, 'connect_retry': 60, 'master_ssl_cipher': None, 'replicate_ignore_db': None, 'master_log_file': 'mysql-bin.000024', 'master_ssl_ca_path': None, 'relay_log_pos': 64659963, 'until_condition': 'None', 'last_io_errno': 0, 'skip_counter': 0, 'replicate_wild_ignore_table': None, 'slave_io_running': True, 'replicate_wild_do_table': None, 'until_log_pos': 0, 'master_ssl_ca_file': None, 'replicate_ignore_table': None, 'master_ssl_verify_server_cert': False, 'replicate_do_table': None, 'replicate_ignore_server_ids': None, 'relay_log_space': 64660762, 'last_io_error': None, 'last_error': None, 'master_server_id': 1, 'replicate_do_db': None}, 'master_status': {'mysql-bin.000024': {'binlog_do_db': None, 'binlog_ignore_db': None, 'position': 64795006, 'file': 'mysql-bin.000024'}}, 'slave_hosts': {'2': {'host': 'i-00000000', 'port': 3306, 'server_id': 2, 'master_id': 1}}, 'status': {'innodb_buffer_pool_pages_free': 7736, 'com_alter_table': 0, 'com_uninstall_plugin': 0, 'key_writes': 0, 'aborted_connects': 13, 'innodb_buffer_pool_wait_free': 0, 'performance_schema_session_connect_attrs_lost': 0, 'sort_scan': 0, 'com_show_collations': 0, 'com_do': 0, 'com_show_fields': 0, 'slow_queries': 0, 'handler_rollback': 0, 'com_create_db': 0, 'com_show_slave_status': 0, 'com_insert_select': 0, 'performance_schema_cond_classes_lost': 0, 'com_show_slave_hosts': 0, 'ssl_server_not_before': None, 'innodb_buffer_pool_reads': 456, 'com_show_create_proc': 0, 'com_revoke': 0, 'performance_schema_hosts_lost': 0, 'key_read_requests': 0, 'com_show_variables': 0, 'handler_discover': 0, 'com_show_grants': 0, 'com_drop_function': 0, 'slave_last_heartbeat': None, 'ssl_accept_renegotiates': 0, 'performance_schema_thread_classes_lost': 0, 'com_show_function_code': 0, 'com_unlock_tables': 0, 'key_reads': 0, 'com_empty_query': 0, 'com_check': 0, 'com_rename_table': 0, 'threads_cached': 0, 'com_xa_recover': 0, 'innodb_data_written': 34304, 'innodb_available_undo_logs': 128, 'qcache_lowmem_prunes': 0, 'ssl_session_cache_overflows': 0, 'ssl_verify_depth': 0, 'com_update_multi': 0, 'questions': 2, 'delayed_writes': 0, 'performance_schema_file_handles_lost': 0, 'key_blocks_not_flushed': 0, 'innodb_row_lock_waits': 0, 'com_xa_end': 0, 'com_xa_prepare': 0, 'com_purge': 0, 'innodb_rows_deleted': 0, 'select_range_check': 0, 'connection_errors_internal': 0, 'com_rollback': 0, 'com_change_master': 0, 'com_show_engine_logs': 0, 'ssl_cipher_list': None, 'com_lock_tables': 0, 'select_full_join': 0, 'com_drop_index': 0, 'com_show_processlist': 0, 'ssl_accepts': 0, 'com_show_create_func': 0, 'innodb_buffer_pool_bytes_dirty': 0, 'performance_schema_locker_lost': 0, 'last_query_partial_plans': 0, 'com_show_tables': 0, 'com_alter_db': 0, 'innodb_dblwr_pages_written': 1, 'com_create_udf': 0, 'slave_running': False, 'com_ha_close': 0, 'handler_mrr_init': 0, 'ssl_session_cache_size': 0, 'performance_schema_accounts_lost': 0, 'com_drop_user': 0, 'connection_errors_max_connections': 0, 'com_set_option': 0, 'com_show_charsets': 0, 'open_files': 18, 'com_signal': 0, 'com_preload_keys': 0, 'com_create_table': 0, 'handler_write': 0, 'com_assign_to_keycache': 0, 'com_create_index': 0, 'com_savepoint': 0, 'handler_prepare': 0, 'opened_files': 118, 'innodb_row_lock_current_waits': 0, 'handler_read_first': 0, 'opened_tables': 0, 'performance_schema_mutex_instances_lost': 0, 'com_alter_tablespace': 0, 'handler_external_lock': 0, 'com_drop_db': 0, 'key_write_requests': 0, 'com_install_plugin': 0, 'com_create_trigger': 0, 'open_table_definitions': 68, 'com_drop_event': 0, 'handler_read_next': 0, 'ssl_session_cache_hits': 0, 'qcache_inserts': 0, 'ssl_used_session_cache_entries': 0, 'ssl_finished_connects': 0, 'com_reset': 0, 'select_range': 0, 'select_scan': 0, 'innodb_rows_read': 0, 'performance_schema_stage_classes_lost': 0, 'com_help': 0, 'innodb_buffer_pool_read_ahead_evicted': 0, 'com_checksum': 0, 'com_show_binlogs': 0, 'com_show_status': 1, 'innodb_buffer_pool_dump_status': 'not started', 'ssl_client_connects': 0, 'com_alter_event': 0, 'com_repair': 0, 'ssl_ctx_verify_mode': 0, 'ssl_callback_cache_hits': 0, 'handler_read_last': 0, 'innodb_os_log_pending_writes': 0, 'select_full_range_join': 0, 'performance_schema_rwlock_instances_lost': 0, 'table_locks_immediate': 74, 'ssl_finished_accepts': 0, 'com_rename_user': 0, 'innodb_buffer_pool_read_ahead_rnd': 0, 'innodb_data_read': 7540736, 'innodb_page_size': 16384, 'binlog_stmt_cache_use': 0, 'com_show_privileges': 0, 'com_execute_sql': 0, 'created_tmp_tables': 0, 'com_xa_commit': 0, 'connections': 148, 'ssl_ctx_verify_depth': 0, 'bytes_received': 224, 'com_show_create_event': 0, 'com_stmt_reprepare': 0, 'com_drop_server': 0, 'com_show_engine_status': 0, 'com_show_plugins': 0, 'connection_errors_accept': 0, 'innodb_have_atomic_builtins': True, 'com_alter_db_upgrade': 0, 'com_get_diagnostics': 0, 'handler_read_key': 0, 'com_show_profiles': 0, 'innodb_buffer_pool_pages_total': 8191, 'com_release_savepoint': 0, 'innodb_truncated_status_writes': 0, 'tc_log_max_pages_used': 0, 'binlog_stmt_cache_disk_use': 0, 'com_delete': 0, 'innodb_os_log_pending_fsyncs': 0, 'binlog_cache_disk_use': 0, 'performance_schema_rwlock_classes_lost': 0, 'delayed_errors': 0, 'innodb_num_open_files': 14, 'com_resignal': 0, 'com_drop_table': 0, 'com_truncate': 0, 'ssl_sessions_reused': 0, 'open_streams': 0, 'performance_schema_statement_classes_lost': 0, 'com_kill': 0, 'com_prepare_sql': 0, 'com_dealloc_sql': 0, 'innodb_buffer_pool_pages_flushed': 1, 'ssl_version': None, 'sort_range': 0, 'com_stmt_fetch': 0, 'performance_schema_socket_classes_lost': 0, 'slave_open_temp_tables': 0, 'com_drop_trigger': 0, 'com_xa_start': 0, 'com_show_keys': 0, 'com_xa_rollback': 0, 'ssl_cipher': None, 'handler_savepoint': 0, 'com_stmt_reset': 0, 'performance_schema_table_handles_lost': 0, 'open_tables': 61, 'handler_commit': 0, 'com_show_create_trigger': 0, 'com_alter_server': 0, 'com_stmt_execute': 0, 'com_select': 1, 'com_commit': 0, 'ssl_session_cache_misses': 0, 'handler_update': 0, 'com_show_create_db': 0, 'table_locks_waited': 0, 'com_stmt_send_long_data': 0, 'performance_schema_users_lost': 0, 'com_replace_select': 0, 'com_flush': 0, 'com_alter_user': 0, 'handler_read_rnd': 0, 'com_create_user': 0, 'com_create_function': 0, 'delayed_insert_threads': 0, 'connection_errors_tcpwrap': 0, 'com_call_procedure': 0, 'innodb_row_lock_time_max': 0, 'innodb_buffer_pool_load_status': 'not started', 'innodb_os_log_written': 512, 'com_show_procedure_status': 0, 'innodb_pages_created': 0, 'qcache_hits': 0, 'qcache_not_cached': 136, 'sort_rows': 0, 'com_admin_commands': 0, 'innodb_row_lock_time': 0, 'innodb_log_write_requests': 0, 'uptime_since_flush_status': 2616535, 'com_show_profile': 0, 'qcache_total_blocks': 1, 'com_stmt_close': 0, 'ssl_connect_renegotiates': 0, 'com_binlog': 0, 'com_alter_procedure': 0, 'compression': False, 'table_open_cache_misses': 0, 'com_update': 0, 'innodb_buffer_pool_pages_dirty': 0, 'created_tmp_files': 5, 'handler_delete': 0, 'com_begin': 0, 'com_create_event': 0, 'innodb_buffer_pool_pages_data': 455, 'innodb_buffer_pool_bytes_data': 7454720, 'slave_received_heartbeats': None, 'ssl_session_cache_timeouts': 0, 'com_purge_before_date': 0, 'com_drop_view': 0, 'performance_schema_mutex_classes_lost': 0, 'innodb_buffer_pool_read_requests': 8252, 'bytes_sent': 168, 'innodb_buffer_pool_write_requests': 1, 'com_ha_read': 0, 'table_open_cache_overflows': 0, 'key_blocks_used': 0, 'com_slave_start': 0, 'table_open_cache_hits': 0, 'com_slave_stop': 0, 'slave_retried_transactions': None, 'com_analyze': 0, 'com_rollback_to_savepoint': 0, 'slow_launch_threads': 0, 'com_show_create_table': 0, 'com_show_open_tables': 0, 'threads_created': 2, 'qcache_free_blocks': 1, 'opened_table_definitions': 0, 'com_optimize': 0, 'performance_schema_file_classes_lost': 0, 'innodb_data_reads': 477, 'com_delete_multi': 0, 'com_insert': 0, 'ssl_verify_mode': 0, 'com_create_procedure': 0, 'innodb_dblwr_writes': 1, 'com_show_procedure_code': 0, 'com_show_databases': 0, 'com_show_relaylog_events': 0, 'last_query_cost': 0.0, 'com_grant': 0, 'handler_read_prev': 0, 'com_alter_function': 0, 'connection_errors_select': 0, 'innodb_pages_read': 455, 'binlog_cache_use': 0, 'innodb_buffer_pool_read_ahead': 0, 'com_drop_procedure': 0, 'ssl_default_timeout': 0, 'queries': 410, 'handler_read_rnd_next': 0, 'innodb_buffer_pool_pages_misc': 0, 'com_show_events': 0, 'com_show_storage_engines': 0, 'com_revoke_all': 0, 'com_ha_open': 0, 'innodb_rows_updated': 0, 'created_tmp_disk_tables': 0, 'innodb_os_log_fsyncs': 3, 'innodb_data_fsyncs': 5, 'com_show_master_status': 0, 'innodb_data_writes': 5, 'flush_commands': 1, 'innodb_pages_written': 1, 'innodb_log_waits': 0, 'sort_merge_passes': 0, 'com_show_table_status': 0, 'tc_log_page_waits': 0, 'performance_schema_cond_instances_lost': 0, 'innodb_rows_inserted': 0, 'threads_running': 1, 'com_show_warnings': 0, 'com_show_binlog_events': 0, 'innodb_data_pending_writes': 0, 'com_show_triggers': 0, 'ssl_session_cache_mode': 'NONE', 'qcache_free_memory': 1031336, 'qcache_queries_in_cache': 0, 'com_show_errors': 0, 'innodb_log_writes': 1, 'com_create_server': 0, 'innodb_data_pending_fsyncs': 0, 'not_flushed_delayed_rows': 0, 'com_load': 0, 'com_change_db': 0, 'tc_log_page_size': 0, 'threads_connected': 2, 'performance_schema_digest_lost': 0, 'innodb_row_lock_time_avg': 0, 'performance_schema_file_instances_lost': 0, 'aborted_clients': 0, 'slave_heartbeat_period': None, 'uptime': 2616535, 'com_show_engine_mutex': 0, 'com_replace': 0, 'performance_schema_table_instances_lost': 0, 'handler_savepoint_rollback': 0, 'com_show_function_status': 0, 'performance_schema_socket_instances_lost': 0, 'com_create_view': 0, 'com_stmt_prepare': 0, 'key_blocks_unused': 6698, 'max_used_connections': 2, 'performance_schema_thread_instances_lost': 0, 'ssl_server_not_after': None, 'rsa_public_key': None, 'connection_errors_peer_address': 0, 'prepared_stmt_count': 0, 'innodb_data_pending_reads': 0}}

### PostgreSQL

Collector for PostgreSQL (http://www.postgresql.org/).

    {'status': {'pg_postmaster_start_time': '2015-05-09 13:06:08.858083+01', 'pg_last_xlog_replay_location': None, 'inet_client_port': 53666, 'pg_backup_start_time': None, 'uptime_s': 16227.606185, 'pg_is_in_backup': False, 'pg_current_xlog_location': '0/308A8CE0', 'pg_backend_pid': 28262, 'pg_is_xlog_replay_paused': None, 'version': 'PostgreSQL 9.4.1 on x86_64-apple-darwin14.3.0, compiled by Apple LLVM version 6.1.0 (clang-602.0.49) (based on LLVM 3.6.0svn), 64-bit', 'inet_server_addr': '127.0.0.1', 'pg_current_xlog_insert_location': '0/308A8CE0', 'pg_is_in_recovery': False, 'pg_last_xlog_receive_location': None, 'inet_server_port': 5432, 'pg_conf_load_time': '2015-05-09 13:06:08.690997+01', 'inet_client_addr': '127.0.0.1', 'pg_last_xact_replay_timestamp': None}, 'stat_replication': {'1114': {'application_name': 'walreceiver', 'sent_location': '0/290044C0', 'sync_priority': 0, 'backend_start': '15-MAY-14 19:54:05.535695 -04:00', 'client_addr': '127.0.0.1', 'backend_xmin': None, 'usename': 'repuser', 'usesysid': 16384, 'write_location': '0/290044C0', 'flush_location': '0/290044C0', 'pid': 1114, 'client_port': 52444, 'sync_state': 'async', 'client_hostname': None, 'replay_location': '0/290044C0', 'state': 'streaming'}}}

### RabbitMQ

Collector for RabbitMQ (https://www.rabbitmq.com).

    {'status': {'run_queue': 0, 'os': ['unix', 'darwin'], 'erlang_version': 'Erlang/OTP 17 [erts-6.1] [source] [64-bit] [smp:4:4] [async-threads:30] [hipe] [kernel-poll:true]\n', 'uptime': 699374, 'listeners': {'amqp': [5672, '127.0.0.1'], 'stomp': [61613, '::'], 'mqtt': [1883, '::'], 'clustering': [25672, '::']}, 'pid': 296, 'vm_memory_high_watermark': 0.4, 'alarms': 'memory', 'disk_free': 272057380864, 'running_applications': {'rabbitmq_amqp1_0': ['AMQP 1.0 support for RabbitMQ', '3.5.1'], 'os_mon': ['CPO  CXC 138 46', '2.2.15'], 'mnesia': ['MNESIA  CXC 138 12', '4.12.1'], 'webmachine': ['webmachine', '1.10.3-rmq3.5.1-gite9359c7'], 'stdlib': ['ERTS  CXC 138 10', '2.1'], 'rabbitmq_management': ['RabbitMQ Management Console', '3.5.1'], 'kernel': ['ERTS  CXC 138 10', '3.0.1'], 'rabbit': ['RabbitMQ', '3.5.1'], 'rabbitmq_stomp': ['Embedded Rabbit Stomp Adapter', '3.5.1'], 'rabbitmq_management_visualiser': ['RabbitMQ Visualiser', '3.5.1'], 'rabbitmq_web_dispatch': ['RabbitMQ Web Dispatcher', '3.5.1'], 'rabbitmq_mqtt': ['RabbitMQ MQTT Adapter', '3.5.1'], 'sasl': ['SASL  CXC 138 11', '2.4'], 'inets': ['INETS  CXC 138 49', '5.10.2'], 'rabbitmq_management_agent': ['RabbitMQ Management Agent', '3.5.1'], 'amqp_client': ['RabbitMQ AMQP Client', '3.5.1'], 'xmerl': ['XML parser', '1.3.7'], 'mochiweb': ['MochiMedia Web Server', '2.7.0-rmq3.5.1-git680dba8']}, 'disk_free_limit': 50000000, 'z_alarms': None, 'file_descriptors': {'total_used': 22, 'sockets_limit': 138, 'sockets_used': 3, 'total_limit': 156}, 'memory': {'connection_other': 5616, 'mnesia': 357864, 'other_ets': 1329520, 'other_proc': 13766976, 'other_system': 5281461, 'code': 20621106, 'mgmt_db': 413992, 'msg_index': 105184, 'total': 43976712, 'atom': 711569, 'connection_writers': 0, 'connection_readers': 0, 'queue_procs': 816560, 'plugins': 548176, 'binary': 18688, 'connection_channels': 0, 'queue_slave_procs': 0}, 'vm_memory_limit': 2804903116, 'processes': {'limit': 1048576, 'used': 274}}, 'cluster_status': {'partitions': {'hare@smacmullen': 'rabbit@smacmullen', 'rabbit@smacmullen': 'hare@smacmullen'}, 'running_nodes': ['rabbit@smacmullen', 'hare@smacmullen'], 'z_partitions': None, 'cluster_name': 'rabbit@tiredpixel.home', 'nodes': {'disc': ['hare@smacmullen', 'rabbit@smacmullen']}}}

### Redis

Collector for Redis (http://redis.io/).

    {'info': {'cpu': {'used_cpu_sys_children': 92.17, 'used_cpu_sys': 4209.35, 'used_cpu_user_children': 1159.56, 'used_cpu_user': 3376.71}, 'stats': {'sync_partial_ok': 0, 'sync_full': 0, 'evicted_keys': 0, 'instantaneous_input_kbps': 0.32, 'instantaneous_ops_per_sec': 4, 'total_net_output_bytes': 17899490797, 'keyspace_misses': 1852618, 'pubsub_patterns': 0, 'total_connections_received': 2574, 'pubsub_channels': 0, 'total_commands_processed': 24187020, 'total_net_input_bytes': 1826548361, 'expired_keys': 22482, 'latest_fork_usec': 3946, 'keyspace_hits': 6123971, 'sync_partial_err': 0, 'instantaneous_output_kbps': 0.08, 'migrate_cached_sockets': 0, 'rejected_connections': 0}, 'clients': {'blocked_clients': 0, 'client_longest_output_list': 0, 'connected_clients': 8, 'client_biggest_input_buf': 0}, 'server': {'redis_git_dirty': 1, 'redis_mode': 'standalone', 'config_file': '/etc/redis/6379.conf', 'multiplexing_api': 'epoll', 'tcp_port': 6379, 'arch_bits': 32, 'redis_git_sha1': '084a59c3', 'lru_clock': 4103598, 'redis_build_id': '4ee713e162d87771', 'uptime_in_days': 51, 'process_id': 3658, 'redis_version': '3.1.999', 'os': 'Linux 3.18.5-x86_64-linode52 x86_64', 'uptime_in_seconds': 4484973, 'gcc_version': '4.4.1', 'hz': 10, 'run_id': 'd2a51d884171bd123e36a03ffcc2d61db7a980d6'}, 'keyspace': {'db0': 'keys=3290,expires=1,avg_ttl=125388596277'}, 'replication': {'repl_backlog_first_byte_offset': 0, 'repl_backlog_size': 1048576, 'repl_backlog_active': 0, 'connected_slaves': 0, 'master_repl_offset': 0, 'role': 'master', 'repl_backlog_histlen': 0}, 'persistence': {'aof_last_write_status': 'ok', 'aof_rewrite_scheduled': 0, 'aof_current_rewrite_time_sec': -1, 'rdb_last_bgsave_time_sec': 0, 'rdb_changes_since_last_save': 481, 'loading': 0, 'aof_enabled': 0, 'rdb_bgsave_in_progress': 0, 'rdb_last_save_time': 1430166862, 'aof_rewrite_in_progress': 0, 'aof_last_rewrite_time_sec': -1, 'rdb_last_bgsave_status': 'ok', 'rdb_current_bgsave_time_sec': -1, 'aof_last_bgrewrite_status': 'ok'}, 'cluster': {'cluster_enabled': 0}, 'memory': {'maxmemory_policy': 'noeviction', 'maxmemory_human': '3.00G', 'total_system_memory_human': '3.91G', 'used_memory_lua_human': '23.00K', 'used_memory_peak': 13159480, 'total_system_memory': 4196720640, 'used_memory': 10752688, 'used_memory_peak_human': '12.55M', 'used_memory_human': '10.25M', 'used_memory_rss_human': '13.42M', 'used_memory_lua': 23552, 'mem_fragmentation_ratio': 1.31, 'used_memory_rss': 14069760, 'maxmemory': 3221225472, 'mem_allocator': 'jemalloc-3.6.0'}}, 'cluster_info': {'cluster_my_epoch': 2, 'cluster_slots_fail': 0, 'cluster_slots_pfail': 0, 'cluster_current_epoch': 6, 'cluster_stats_messages_sent': 1483972, 'cluster_size': 3, 'cluster_slots_assigned': 16384, 'cluster_stats_messages_received': 1483968, 'cluster_known_nodes': 6, 'cluster_state': 'ok', 'cluster_slots_ok': 16384}}


## Design

One of the design goals of Pikka Bird is to enable production-suitable setup in
a minimum of steps and configuration. To support this, Pikka Bird supports as
many services as possible without requiring further dependencies, regardless of
whether those services are installed or even compatible with the server.

For this reason, shelling out and using service executables directly is
preferred to adding library dependencies (e.g. [PostgreSQL][postgresql]
`psql` to be used instead of using a nice library binding). This is slower, and
can cause juggling with paths and different systems and shells, but enables
the core dependencies to be kept small whilst allowing the supported services to
grow into the tens or hundreds.

Pikka Bird is designed to gather and send as many metrics as can be found (with
selective configuration at a collector level), even if that leads to large
reports. Pikka Bird Collector has no concept of success or failure of individual
metrics. Think more like a squirrel gathering nuts in a forest than asking the
server whether it is okay by means of executed checks. This, at the expense of
storage and some speed, does away with problems of remote execution privileges
or installing and maintaining remote checks, as all interpretive dance occurs in
the Server component on a fixed data structure.


## Development

Copy the example configuration for development, adjusting to taste:

    cp .env.example .env

Copy the example configuration for testing, adjusting to taste, adding the
environment variable `CI=true` (the tests are destructive to the database):

    cp .env.example .test.env

Install locally using [Pip][pip] editable mode:

    pip install -r requirements.txt
    pip install -e .

Start a collector eternally using [Honcho][honcho], which reads `Procfile`:

    honcho start

Run the tests, which use [py.test][py_test]:

    honcho run -e .test.env py.test


## Stay Tuned

We have a [Librelist][librelist] mailing list!
To subscribe, send an email to <pikka.bird@librelist.com>.
To unsubscribe, send an email to <pikka.bird-unsubscribe@librelist.com>.
There be [archives](http://librelist.com/browser/pikka.bird/).

You can also become a
[watcher](https://github.com/tiredpixel/pikka-bird-collector/watchers)
on GitHub. And don't forget you can become a
[stargazer](https://github.com/tiredpixel/pikka-bird-collector/stargazers)
if you are so minded. :D


## Contributions

Contributions are embraced with much love and affection! <3 Please fork the
repository and wizard your magic, preferably with plenty of fairy-dust sprinkled
over the tests. Then send me a pull request. :) If you're thinking about
working on something involved, it would be great if you could wave via the
issue tracker or mailing list; I'd hate for good effort to be wasted!

Do whatever makes you happy. We'll probably still like you. :)


## Blessing

May you find peace, and help others to do likewise.


## Licence

© [tiredpixel](https://www.tiredpixel.com/) 2015.
It is free software, released under the MIT License, and may be redistributed
under the terms specified in `LICENSE.txt`.


[honcho]: https://github.com/nickstenning/honcho
[librelist]: http://librelist.com/
[pip]: https://pypi.python.org/pypi/pip
[postgresql]: http://www.postgresql.org/
[py_test]: http://pytest.org/latest/
[python]: https://www.python.org/
[server]: https://github.com/tiredpixel/pikka-bird-server-py
