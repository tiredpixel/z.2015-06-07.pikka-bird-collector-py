import os

from pikka_bird_collector.collectors.rabbitmq import Rabbitmq
from pikka_bird_collector.collectors.base_port_command import BasePortCommand


class TestRabbitmq:
    
    @staticmethod
    def fixture_path(filename):
        return os.path.join(os.path.dirname(__file__), '../fixtures', filename)
    
    @staticmethod
    def read_fixture(filename):
        with open(filename, 'r') as f_h:
            d = f_h.read()
        return d
    
    def mock_cmd_status(self):
        f = TestRabbitmq.fixture_path('rabbitmq/status.erl')
        return TestRabbitmq.read_fixture(f)
    
    def mock_cmd_cluster_status(self):
        f = TestRabbitmq.fixture_path('rabbitmq/cluster_status.erl')
        return TestRabbitmq.read_fixture(f)
    
    def mock_collect_status(self):
        return {
            'pid': 296,
            'running_applications': {
                'rabbitmq_management_visualiser': [
                    "RabbitMQ Visualiser",
                    "3.5.1"],
                'rabbitmq_management': [
                    "RabbitMQ Management Console",
                    "3.5.1"],
                'rabbitmq_web_dispatch': [
                    "RabbitMQ Web Dispatcher",
                    "3.5.1"],
                'webmachine': [
                    "webmachine",
                    "1.10.3-rmq3.5.1-gite9359c7"],
                'mochiweb': [
                    "MochiMedia Web Server",
                    "2.7.0-rmq3.5.1-git680dba8"],
                'rabbitmq_mqtt': [
                    "RabbitMQ MQTT Adapter",
                    "3.5.1"],
                'rabbitmq_stomp': [
                    "Embedded Rabbit Stomp Adapter",
                    "3.5.1"],
                'rabbitmq_management_agent': [
                    "RabbitMQ Management Agent",
                    "3.5.1"],
                'rabbitmq_amqp1_0': [
                    "AMQP 1.0 support for RabbitMQ",
                    "3.5.1"],
                'rabbit': [
                    "RabbitMQ",
                    "3.5.1"],
                'os_mon': [
                    "CPO  CXC 138 46",
                    "2.2.15"],
                'inets': [
                    "INETS  CXC 138 49",
                    "5.10.2"],
                'mnesia': [
                    "MNESIA  CXC 138 12",
                    "4.12.1"],
                'amqp_client': [
                    "RabbitMQ AMQP Client",
                    "3.5.1"],
                'xmerl': [
                    "XML parser",
                    "1.3.7"],
                'sasl': [
                    "SASL  CXC 138 11",
                    "2.4"],
                'stdlib': [
                    "ERTS  CXC 138 10",
                    "2.1"],
                'kernel': [
                    "ERTS  CXC 138 10",
                    "3.0.1"]},
            'os': [
                'unix',
                'darwin'],
            'erlang_version': "Erlang/OTP 17 [erts-6.1] [source] [64-bit] [smp:4:4] [async-threads:30] [hipe] [kernel-poll:true]\n",
            'memory': {
                'total': 43976712,
                'connection_readers': 0,
                'connection_writers': 0,
                'connection_channels': 0,
                'connection_other': 5616,
                'queue_procs': 816560,
                'queue_slave_procs': 0,
                'plugins': 548176,
                'other_proc': 13766976,
                'mnesia': 357864,
                'mgmt_db': 413992,
                'msg_index': 105184,
                'other_ets': 1329520,
                'binary': 18688,
                'code': 20621106,
                'atom': 711569,
                'other_system': 5281461},
            'alarms': 'memory',
            'z_alarms': None,
            'listeners': {
                'clustering': [
                    25672,
                    "::"],
                'amqp': [
                    5672,
                    "127.0.0.1"],
                'stomp': [
                    61613,
                    "::"],
                'mqtt': [
                    1883,
                    "::"]},
            'vm_memory_high_watermark': 0.4,
            'vm_memory_limit': 2804903116,
            'disk_free_limit': 50000000,
            'disk_free': 272057380864,
            'file_descriptors': {
                'total_limit': 156,
                'total_used': 22,
                'sockets_limit': 138,
                'sockets_used': 3},
            'processes': {
                'limit': 1048576,
                'used': 274},
            'run_queue': 0,
            'uptime': 699374}
    
    def mock_collect_cluster_status(self):
        return {
            'nodes': {
                'disc': [
                    "hare@smacmullen",
                    "rabbit@smacmullen"]},
            'running_nodes': [
                "rabbit@smacmullen",
                "hare@smacmullen"],
            'cluster_name': "rabbit@tiredpixel.home",
            'z_partitions': None,
            'partitions': {
                'rabbit@smacmullen': "hare@smacmullen",
                'hare@smacmullen': "rabbit@smacmullen"}}
    
    def mock_exec_command(self, command_f):
        command = command_f[-1]
        if command == Rabbitmq.CMD_CLUSTER_STATUS:
            return self.mock_cmd_cluster_status()
        elif command == Rabbitmq.CMD_STATUS:
            return self.mock_cmd_status()
    
    def test_command_tool(self):
        assert (Rabbitmq.command_tool(5672, {}, 'status') ==
            ['rabbitmqctl', '-q', 'status'])
    
    def test_enabled(self):
        rabbitmq = Rabbitmq({}, { 5672: {} })
        
        assert rabbitmq.enabled() == True
    
    def test_enabled_no_ports(self):
        rabbitmq = Rabbitmq({}, {})
        
        assert rabbitmq.enabled() == False
    
    def test_collect(self, monkeypatch):
        monkeypatch.setattr(BasePortCommand, 'exec_command',
            self.mock_exec_command)
        
        rabbitmq = Rabbitmq({}, { 5672: {} })
        metrics = rabbitmq.collect()
        
        metrics_t = {
            'status':         self.mock_collect_status(),
            'cluster_status': self.mock_collect_cluster_status()}
        
        assert metrics[5672] == metrics_t
        
        for setting in Rabbitmq.COLLECT_SETTING_DEFAULTS.keys():
            rabbitmq2 = Rabbitmq({}, { 5672: { 'collect': { setting: False } } })
            metrics2 = rabbitmq2.collect()
            
            metrics_t2 = metrics_t.copy()
            del metrics_t2[setting]
            assert metrics2[5672] == metrics_t2
