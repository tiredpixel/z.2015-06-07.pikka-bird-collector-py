import os
import collections
import psutil

from pikka_bird_collector.collectors.system import System


class TestSystem:
    
    def mock_getloadavg(self):
        return (42, 84, 126)
    
    def mock_statvfs(self, mount):
        MockStatvfs = collections.namedtuple('MockStatvfs', [
            'f_bsize',
            'f_frsize',
            'f_blocks',
            'f_bfree',
            'f_bavail',
            'f_files',
            'f_ffree',
            'f_favail',
            'f_flag',
            'f_namemax'])
        
        return MockStatvfs(
            f_bsize=1764,
            f_frsize=1765,
            f_blocks=42,
            f_bfree=74088,
            f_bavail=1768,
            f_files=1769,
            f_ffree=130691232,
            f_favail=3111696,
            f_flag=1772,
            f_namemax=1773)
    
    def mock_disk_partitions(self, all=False):
        MockDiskPartition = collections.namedtuple('MockDiskPartition', [
            'device',
            'mountpoint',
            'fstype',
            'opts'])
        
        return [MockDiskPartition(
            device='/dev/disk42',
            mountpoint='/',
            fstype='zaphod',
            opts='rw,local,rootfs,dovolfs,journaled,multilabel,interplanetary')]
    
    def mock_disk_usage(self, mount):
        MockDiskUsage = collections.namedtuple('MockDiskUsage', [
            'total',
            'used',
            'free',
            'percent'])
        
        return MockDiskUsage(
            total=100440011101,
            used=1800538114,
            free=98639472987,
            percent=0.01)
    
    def test_enabled(self):
        system = System({})
        
        assert system.enabled() == True
    
    def test_collect_live(self):
        system = System({})
        metrics = system.collect()
        
        metrics_load = metrics['system']['load']
        
        assert type(metrics_load['avg_1_min']) == float
        assert type(metrics_load['avg_5_min']) == float
        assert type(metrics_load['avg_15_min']) == float
        
        metrics_disk = metrics['system']['disk']['/']
        
        assert type(metrics_disk['block_size_b']) == int
        assert type(metrics_disk['fragment_size_b']) == int
        assert type(metrics_disk['blocks']) == int
        assert type(metrics_disk['blocks_free']) == int
        assert type(metrics_disk['blocks_free_/']) == float
        assert type(metrics_disk['blocks_free_unpriv']) == int
        assert type(metrics_disk['blocks_free_unpriv_/']) == float
        assert type(metrics_disk['inodes']) == int
        assert type(metrics_disk['inodes_free']) == int
        assert type(metrics_disk['inodes_free_/']) == float
        assert type(metrics_disk['inodes_free_unpriv']) == int
        assert type(metrics_disk['inodes_free_unpriv_/']) == float
        assert type(metrics_disk['flags']) == int
        assert type(metrics_disk['filename_len_max']) == int
        assert type(metrics_disk['device']) == str
        assert type(metrics_disk['fstype']) == str
        assert type(metrics_disk['space_b']) == int
        assert type(metrics_disk['space_used_b']) == int
        assert type(metrics_disk['space_used_/']) == float
        assert type(metrics_disk['space_free_b']) == int
        assert type(metrics_disk['space_free_/']) == float
    
    def test_collect_mocked(self, monkeypatch):
        monkeypatch.setattr(os, 'getloadavg', self.mock_getloadavg)
        monkeypatch.setattr(os, 'statvfs', self.mock_statvfs)
        monkeypatch.setattr(psutil, 'disk_partitions', self.mock_disk_partitions)
        monkeypatch.setattr(psutil, 'disk_usage', self.mock_disk_usage)
        
        system = System({})
        metrics = system.collect()
        
        # round floats (like beach balls)
        for metric in [
            'blocks_free_/',
            'blocks_free_unpriv_/',
            'inodes_free_/',
            'inodes_free_unpriv_/',
            'space_used_/',
            'space_free_/']:
            metrics['system']['disk']['/'][metric] = round(
                    metrics['system']['disk']['/'][metric], 2)
        
        assert metrics == {
            'system': {
                'load': {
                    'avg_1_min': 42,
                    'avg_5_min': 84,
                    'avg_15_min': 126},
                'disk': {
                    '/': {
                        'block_size_b': 1764,
                        'fragment_size_b': 1765,
                        'blocks': 42,
                        'blocks_free': 74088,
                        'blocks_free_/': 1764.0,
                        'blocks_free_unpriv': 1768,
                        'blocks_free_unpriv_/': 42.1,
                        'inodes': 1769,
                        'inodes_free': 130691232,
                        'inodes_free_/': 73878.59,
                        'inodes_free_unpriv': 3111696,
                        'inodes_free_unpriv_/': 1759.01,
                        'flags': 1772,
                        'filename_len_max': 1773,
                        'device': '/dev/disk42',
                        'fstype': 'zaphod',
                        'space_b': 100440011101,
                        'space_used_b': 1800538114,
                        'space_used_/': 0.02,
                        'space_free_b': 98639472987,
                        'space_free_/': 0.98}}}}
    
    def test_collect_load_oserror(self, monkeypatch):
        def mock_getloadavg():
            raise OSError
        
        monkeypatch.setattr(os, 'getloadavg', mock_getloadavg)
        
        system = System({})
        metrics = system.collect()
        
        assert metrics['system']['load'] == {}
    
    def test_collect_disk_statvfs_filenotfounderror(self, monkeypatch):
        def mock_statvfs(mount):
            raise FileNotFoundError
        
        monkeypatch.setattr(os, 'statvfs', mock_statvfs)
        
        system = System({})
        metrics = system.collect()
        
        assert metrics['system']['disk']['/'] == {}
    
    def test_collect_disk_disk_usage_oserror(self, monkeypatch):
        def mock_disk_usage(mount):
            raise OSError
        
        monkeypatch.setattr(psutil, 'disk_usage', mock_disk_usage)
        
        system = System({})
        metrics = system.collect()
        
        assert metrics['system']['disk']['/'] == {}
