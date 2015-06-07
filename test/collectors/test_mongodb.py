import os

from pikka_bird_collector.collectors.mongodb import Mongodb
from pikka_bird_collector.collectors.base_port_command import BasePortCommand


class TestMongodb:
    
    @staticmethod
    def fixture_path(filename):
        return os.path.join(os.path.dirname(__file__), '../fixtures', filename)
    
    @staticmethod
    def read_fixture(filename):
        with open(filename, 'r') as f_h:
            d = f_h.read()
        return d
    
    def mock_cmd_db_server_status(self):
        f = TestMongodb.fixture_path('mongodb/db_server_status.js')
        return TestMongodb.read_fixture(f)
    
    def mock_cmd_rs_status(self):
        f = TestMongodb.fixture_path('mongodb/rs_status.js')
        return TestMongodb.read_fixture(f)
    
    def mock_exec_command(self, command_f):
        if Mongodb.CMD_DB_SERVER_STATUS in command_f:
            return self.mock_cmd_db_server_status()
        elif Mongodb.CMD_RS_STATUS in command_f:
            return self.mock_cmd_rs_status()
    
    def mock_collect_server_status(self):
        return {
            'asserts': {
                'msg': 0,
                'regular': 0,
                'rollovers': 0,
                'user': 0,
                'warning': 0},
            'backgroundFlushing': {
                'average_ms': 4.1476367498672335,
                'flushes': 1883,
                'last_finished': '2015-05-16T15:45:53.346Z',
                'last_ms': 5,
                'total_ms': 7810},
            'connections': {
                'available': 202,
                'current': 2,
                'totalCreated': 28},
            'cursors': {
                'clientCursors_size': 0,
                'note': 'deprecated, use server status metrics',
                'pinned': 0,
                'timedOut': 0,
                'totalNoTimeout': 0,
                'totalOpen': 0},
            'dur': {
                'commits': 10,
                'commitsInWriteLock': 0,
                'compression': 0,
                'earlyCommits': 0,
                'journaledMB': 0,
                'timeMs': {
                    'commits': 0,
                    'commitsInWriteLock': 0,
                    'dt': 3067,
                    'prepLogBuffer': 0,
                    'remapPrivateView': 0,
                    'writeToDataFiles': 0,
                    'writeToJournal': 0},
                'writeToDataFilesMB': 0},
            'extra_info': {
                'note': 'fields vary by platform',
                'page_faults': 175428},
            'globalLock': {
                'activeClients': {
                    'readers': 0,
                    'total': 10,
                    'writers': 0},
                'currentQueue': {
                    'readers': 0,
                    'total': 0,
                    'writers': 0},
                'totalTime': '618021658000'},
            'host': 'tiredpixel.home',
            'localTime': '2015-05-16T15:46:30.380Z',
            'locks': {
                'Collection': {
                    'acquireCount': {
                        'R': 385078}},
                'Database': {
                    'acquireCount': {
                        'R': 6,
                        'W': 15,
                        'r': 366251}},
                'Global': {
                    'acquireCount': {
                        'W': 5,
                        'r': 366257,
                        'w': 15}},
                'MMAPV1Journal': {
                    'acquireCount': {
                        'R': 354821,
                        'r': 366255,
                        'w': 35},
                    'acquireWaitCount': {
                        'R': 4,
                        'w': 3},
                    'timeAcquiringMicros': {
                        'R': 7163519,
                        'w': 131}},
                'Metadata': {
                    'acquireCount': {
                        'R': 1}}},
            'mem': {
                'bits': 64,
                'mapped': 240,
                'mappedWithJournal': 480,
                'resident': 50,
                'supported': True,
                'virtual': 2973},
            'metrics': {
                'commands': {
                    '<UNKNOWN>': 4,
                    'dbStats': {
                        'failed': 1,
                        'total': 4},
                    'getLog': {
                        'failed': 0,
                        'total': 8},
                    'getnonce': {
                        'failed': 0,
                        'total': 2},
                    'isMaster': {
                        'failed': 0,
                        'total': 34},
                    'listDatabases': {
                        'failed': 0,
                        'total': 1},
                    'ping': {
                        'failed': 0,
                        'total': 4},
                    'replSetGetStatus': {
                        'failed': 16,
                        'total': 16},
                    'serverStatus': {
                        'failed': 0,
                        'total': 15},
                    'top': {
                        'failed': 0,
                        'total': 5},
                    'whatsmyuri': {
                        'failed': 0,
                        'total': 26}},
                'cursor': {
                    'open': {
                        'noTimeout': 0,
                        'pinned': 0,
                        'total': 0},
                    'timedOut': 0},
                'document': {
                    'deleted': 0,
                    'inserted': 0,
                    'returned': 0,
                    'updated': 0},
                'getLastError': {
                    'wtime': {
                        'num': 0,
                        'totalMillis': 0},
                    'wtimeouts': 0},
                'operation': {
                    'fastmod': 0,
                    'idhack': 0,
                    'scanAndOrder': 0,
                    'writeConflicts': 0},
                'queryExecutor': {
                    'scanned': 0,
                    'scannedObjects': 0},
                'record': {
                    'moves': 0},
                'repl': {
                    'apply': {
                        'batches': {
                            'num': 0,
                            'totalMillis': 0},
                        'ops': 0},
                    'buffer': {
                        'count': 0,
                        'maxSizeBytes': 268435456,
                        'sizeBytes': 0},
                    'network': {
                        'bytes': 0,
                        'getmores': {
                            'num': 0,
                            'totalMillis': 0},
                        'ops': 0,
                        'readersCreated': 0},
                    'preload': {
                        'docs': {
                            'num': 0,
                            'totalMillis': 0},
                        'indexes': {
                            'num': 0,
                            'totalMillis': 0}}},
                'storage': {
                    'freelist': {
                        'search': {
                            'bucketExhausted': 0,
                            'requests': 0,
                            'scanned': 0}}},
                'ttl': {
                    'deletedDocuments': 0,
                    'passes': 1883}},
            'network': {
                'bytesIn': 8422,
                'bytesOut': 182467,
                'numRequests': 120},
            'ok': 1,
            'opcounters': {
                'command': 115,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 2,
                'update': 0},
            'opcountersRepl': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0},
            'pid': 286,
            'process': 'mongod',
            'storageEngine': {
                'name': 'mmapv1'},
            'uptime': 618022,
            'uptimeEstimate': 22874,
            'uptimeMillis': 618021690,
            'version': '3.0.2',
            'writeBacksQueued': False}
    
    def mock_collect_rs_status(self):
        return {
            'date': '2014-05-01T14:44:03Z',
            'members': [
                {
                    '_id': 0,
                    'electionDate': '2014-05-01T14:39:46Z',
                    'electionTime': 1404225586,
                    'health': 1,
                    'name': 'm1.example.net:27017',
                    'optime': 1404225575,
                    'optimeDate': '2014-05-01T14:39:35Z',
                    'self': True,
                    'state': 1,
                    'stateStr': 'PRIMARY',
                    'uptime': 269},
                {
                    '_id': 1,
                    'health': 1,
                    'lastHeartbeat': '2014-05-01T14:44:03Z',
                    'lastHeartbeatRecv': '2014-05-01T14:44:02Z',
                    'name': 'm2.example.net:27017',
                    'optime': 1404225575,
                    'optimeDate': '2014-05-01T14:39:35Z',
                    'pingMs': 0,
                    'state': 2,
                    'stateStr': 'SECONDARY',
                    'syncingTo': 'm1.example.net:27017',
                    'uptime': 265},
                {
                    '_id': 2,
                    'health': 1,
                    'lastHeartbeat': '2014-05-01T14:44:02Z',
                    'lastHeartbeatRecv': '2014-05-01T14:44:02Z',
                    'name': 'm3.example.net:27017',
                    'optime': 1404225575,
                    'optimeDate': '2014-05-01T14:39:35Z',
                    'pingMs': 0,
                    'state': 2,
                    'stateStr': 'SECONDARY',
                    'syncingTo': 'm1.example.net:27017',
                    'uptime': 265}],
            'myState': 1,
            'ok': 1,
            'set': 'replset'}
    
    def test_command_tool(self):
        assert (Mongodb.command_tool(27017, {}, 'printjson()') ==
            ['mongo', '--port', 27017,
                '--eval', 'printjson()',
                '--quiet'])
    
    def test_command_tool_user(self):
        assert (Mongodb.command_tool(27017, { 'user': "USER" }, 'printjson()') ==
            ['mongo', '--port', 27017,
                '--eval', 'printjson()',
                '--quiet',
                '--username', 'USER'])
    
    def test_command_tool_password(self):
        assert (Mongodb.command_tool(27017, { 'password': "PASSWORD" }, 'printjson()') ==
            ['mongo', '--port', 27017,
                '--eval', 'printjson()',
                '--quiet',
                '--password', 'PASSWORD'])
    
    def test_enabled(self):
        mongodb = Mongodb({}, { 27017: {} })
        
        assert mongodb.enabled() == True
    
    def test_enabled_no_ports(self):
        mongodb = Mongodb({}, {})
        
        assert mongodb.enabled() == False
    
    def test_collect(self, monkeypatch):
        monkeypatch.setattr(BasePortCommand, 'exec_command',
            self.mock_exec_command)
        
        mongodb = Mongodb({}, { 27017: {} })
        metrics = mongodb.collect()
        
        metrics_t = {
            'server_status': self.mock_collect_server_status(),
            'rs_status':     self.mock_collect_rs_status()}
        
        assert metrics[27017] == metrics_t
        
        for setting in Mongodb.COLLECT_SETTING_DEFAULTS.keys():
            mongodb2 = Mongodb({}, { 27017: {
                'collect': { setting: False } } })
            metrics2 = mongodb2.collect()
            
            metrics_t2 = metrics_t.copy()
            del metrics_t2[setting]
            assert metrics2[27017] == metrics_t2
