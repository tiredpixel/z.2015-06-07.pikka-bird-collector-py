import os

from pikka_bird_collector.collectors.redis import Redis
from pikka_bird_collector.collectors.base_port_command import BasePortCommand


class TestRedis:
    
    @staticmethod
    def fixture_path(filename):
        return os.path.join(os.path.dirname(__file__), '../fixtures', filename)
    
    @staticmethod
    def read_fixture(filename):
        with open(filename, 'r') as f_h:
            d = f_h.read()
        return d
    
    def mock_error(self):
        f = TestRedis.fixture_path('redis/error.txt')
        return TestRedis.read_fixture(f)
    
    def mock_cmd_info(self):
        f = TestRedis.fixture_path('redis/info.txt')
        return TestRedis.read_fixture(f)
    
    def mock_cmd_cluster_info(self):
        f = TestRedis.fixture_path('redis/cluster_info.txt')
        return TestRedis.read_fixture(f)
    
    def mock_collect_info(self):
        return {
            'clients': {
                'blocked_clients': 0,
                'client_biggest_input_buf': 0,
                'client_longest_output_list': 0,
                'connected_clients': 8},
            'cluster': {
                'cluster_enabled': 0},
            'cpu': {
                'used_cpu_sys': 4209.35,
                'used_cpu_sys_children': 92.17,
                'used_cpu_user': 3376.71,
                'used_cpu_user_children': 1159.56},
            'keyspace': {
                'db0': 'keys=3290,expires=1,avg_ttl=125388596277'},
            'memory': {
                'maxmemory': 3221225472,
                'maxmemory_human': '3.00G',
                'maxmemory_policy': 'noeviction',
                'mem_allocator': 'jemalloc-3.6.0',
                'mem_fragmentation_ratio': 1.31,
                'total_system_memory': 4196720640,
                'total_system_memory_human': '3.91G',
                'used_memory': 10752688,
                'used_memory_human': '10.25M',
                'used_memory_lua': 23552,
                'used_memory_lua_human': '23.00K',
                'used_memory_peak': 13159480,
                'used_memory_peak_human': '12.55M',
                'used_memory_rss': 14069760,
                'used_memory_rss_human': '13.42M'},
            'persistence': {
                'aof_current_rewrite_time_sec': -1,
                'aof_enabled': 0,
                'aof_last_bgrewrite_status': 'ok',
                'aof_last_rewrite_time_sec': -1,
                'aof_last_write_status': 'ok',
                'aof_rewrite_in_progress': 0,
                'aof_rewrite_scheduled': 0,
                'loading': 0,
                'rdb_bgsave_in_progress': 0,
                'rdb_changes_since_last_save': 481,
                'rdb_current_bgsave_time_sec': -1,
                'rdb_last_bgsave_status': 'ok',
                'rdb_last_bgsave_time_sec': 0,
                'rdb_last_save_time': 1430166862},
            'replication': {
                'connected_slaves': 0,
                'master_repl_offset': 0,
                'repl_backlog_active': 0,
                'repl_backlog_first_byte_offset': 0,
                'repl_backlog_histlen': 0,
                'repl_backlog_size': 1048576,
                'role': 'master'},
            'server': {
                'arch_bits': 32,
                'config_file': '/etc/redis/6379.conf',
                'gcc_version': '4.4.1',
                'hz': 10,
                'lru_clock': 4103598,
                'multiplexing_api': 'epoll',
                'os': 'Linux 3.18.5-x86_64-linode52 x86_64',
                'process_id': 3658,
                'redis_build_id': '4ee713e162d87771',
                'redis_git_dirty': 1,
                'redis_git_sha1': '084a59c3',
                'redis_mode': 'standalone',
                'redis_version': '3.1.999',
                'run_id': 'd2a51d884171bd123e36a03ffcc2d61db7a980d6',
                'tcp_port': 6379,
                'uptime_in_days': 51,
                'uptime_in_seconds': 4484973},
            'stats': {
                'evicted_keys': 0,
                'expired_keys': 22482,
                'instantaneous_input_kbps': 0.32,
                'instantaneous_ops_per_sec': 4,
                'instantaneous_output_kbps': 0.08,
                'keyspace_hits': 6123971,
                'keyspace_misses': 1852618,
                'latest_fork_usec': 3946,
                'migrate_cached_sockets': 0,
                'pubsub_channels': 0,
                'pubsub_patterns': 0,
                'rejected_connections': 0,
                'sync_full': 0,
                'sync_partial_err': 0,
                'sync_partial_ok': 0,
                'total_commands_processed': 24187020,
                'total_connections_received': 2574,
                'total_net_input_bytes': 1826548361,
                'total_net_output_bytes': 17899490797}}
    
    def mock_collect_cluster_info(self):
        return {
            'cluster_my_epoch': 2,
            'cluster_slots_pfail': 0,
            'cluster_current_epoch': 6,
            'cluster_state': 'ok',
            'cluster_size': 3,
            'cluster_slots_ok': 16384,
            'cluster_slots_assigned': 16384,
            'cluster_stats_messages_sent': 1483972,
            'cluster_slots_fail': 0,
            'cluster_stats_messages_received': 1483968,
            'cluster_known_nodes': 6}
    
    def mock_exec_command(self, command_f):
        command = command_f[-1]
        if command == Redis.CMD_CLUSTER_INFO:
            return self.mock_cmd_cluster_info()
        elif command == Redis.CMD_INFO:
            return self.mock_cmd_info()
    
    def test_command_tool(self):
        assert (Redis.command_tool(6379, {}, 'INFO') ==
            ['redis-cli', '-p', 6379, 'INFO'])
    
    def test_command_tool_password(self):
        assert (Redis.command_tool(6380, { 'password': "PW" }, 'DBSIZE') ==
            ['redis-cli', '-p', 6380, '-a', 'PW', 'DBSIZE'])
    
    def test_parse_output_none(self):
        assert Redis.parse_output(None) == {}
    
    def test_parse_output_error(self):
        assert Redis.parse_output(self.mock_error()) == {}
    
    def test_parse_output_info(self):
        assert (Redis.parse_output(self.mock_cmd_info()) ==
            self.mock_collect_info())
    
    def test_parse_output_cluster_info(self):
        assert (Redis.parse_output(self.mock_cmd_cluster_info()) ==
            self.mock_collect_cluster_info())
    
    def test_enabled(self):
        redis = Redis({}, { 6379: {} })
        
        assert redis.enabled() == True
    
    def test_enabled_no_ports(self):
        redis = Redis({}, {})
        
        assert redis.enabled() == False
    
    def test_collect(self, monkeypatch):
        monkeypatch.setattr(BasePortCommand, 'exec_command', self.mock_exec_command)
        
        redis = Redis({}, { 6379: {} })
        metrics = redis.collect()
        
        assert metrics == {
            6379: {
                'info':         self.mock_collect_info(),
                'cluster_info': self.mock_collect_cluster_info()}}
    
    def test_collect_no_cluster_info(self, monkeypatch):
        monkeypatch.setattr(BasePortCommand, 'exec_command', self.mock_exec_command)
        
        redis = Redis({}, { 6379: { 'cluster_info': False } })
        metrics = redis.collect()
        
        assert metrics == {
            6379: {
                'info': self.mock_collect_info()}}
