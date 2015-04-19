import os
import platform
import socket

import pikka_bird_collector
from pikka_bird_collector.collector import Collector


class TestCollector:
    
    def mock_system(self):
        return "Hovercraft"
    
    def mock_release(self):
        return "42.21.11"
    
    def mock_version(self):
        return "Hovercraft Kernel Version 42.21.11 128-bit"
    
    def test_collect_live(self):
        collector = Collector()
        collection = collector.collect()
        
        assert type(collection['collecting_at']) == str
        assert type(collection['collected_at']) == str
        
        assert collection['environment']['hostname'] == socket.gethostname()
        assert collection['environment']['pid'] == os.getpid()
        assert collection['environment']['version'] == pikka_bird_collector.__version__
        assert type(collection['environment']['platform']['system']) == str
        assert type(collection['environment']['platform']['release']) == str
        assert type(collection['environment']['platform']['version']) == str
        
        assert type(collection['reports']) == dict
        assert type(collection['reports']['system']) == dict
        
        assert len(collection) == 4
        assert len(collection['environment']) == 4
        assert len(collection['environment']['platform']) == 3
        assert len(collection['reports']) == 1
    
    def test_collect_mocked(self, monkeypatch):
        monkeypatch.setattr(platform, 'system', self.mock_system)
        monkeypatch.setattr(platform, 'release', self.mock_release)
        monkeypatch.setattr(platform, 'version', self.mock_version)
        
        collector = Collector()
        collection = collector.collect()
        
        assert type(collection['collecting_at']) == str
        assert type(collection['collected_at']) == str
        
        assert collection['environment'] == {
            'hostname': socket.gethostname(),
            'pid':      os.getpid(),
            'version':  pikka_bird_collector.__version__,
            'platform': {
                'system':  "Hovercraft",
                'release': "42.21.11",
                'version': "Hovercraft Kernel Version 42.21.11 128-bit"}}
        
        assert type(collection['reports']) == dict
        assert type(collection['reports']['system']) == dict
        
        assert len(collection) == 4
        assert len(collection['environment']) == 4
        assert len(collection['environment']['platform']) == 3
        assert len(collection['reports']) == 1
