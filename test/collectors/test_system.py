import os
import collections
import psutil

from pikka_bird_collector.collectors.system import System


class TestSystem:
    
    def mock_getloadavg(self):
        return (42.0, 84.0, 126.0)
    
    def mock_cpu_times_percent(self, interval=None, percpu=False):
        MockCpuTimesPercent = collections.namedtuple('MockCpuTimesPercent', [
            'user',
            'system',
            'idle',
            'nice',
            'iowait',
            'irq',
            'softirq',
            'steal',
            'guest',
            'guest_nice'])
        
        return [MockCpuTimesPercent(
            user=1,
            system=2,
            idle=55,
            nice=3,
            iowait=4,
            irq=5,
            softirq=6,
            steal=7,
            guest=8,
            guest_nice=9)]
    
    def mock_virtual_memory(self):
        MockVirtualMemory = collections.namedtuple('MockVirtualMemory', [
            'total',
            'available',
            'used',
            'free',
            'active',
            'inactive',
            'buffers',
            'cached',
            'wired',
            'shared'])
        
        return MockVirtualMemory(
            total=8589934592,
            available=4248592384,
            used=4688113664,
            free=3279757312,
            active=2415570944,
            inactive=968835072,
            buffers=258020000,
            cached=241716800,
            wired=1303707648,
            shared=50448000)
    
    def mock_swap_memory(self):
        MockSwapMemory = collections.namedtuple('MockSwapMemory', [
            'total',
            'used',
            'free',
            'sin',
            'sout'])
        
        return MockSwapMemory(
            total=2147483648,
            used=1196949504,
            free=950534144,
            sin=66084589568,
            sout=1213657088)
    
    def mock_swap_memory_zero_total(self):
        MockSwapMemory = collections.namedtuple('MockSwapMemory', [
            'total',
            'used',
            'free',
            'sin',
            'sout'])
        
        return MockSwapMemory(
            total=0,
            used=1196949504,
            free=950534144,
            sin=66084589568,
            sout=1213657088)
    
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
        system = System({}, {})
        
        assert system.enabled() == True
    
    def test_collect_live(self):
        system = System({}, {})
        metrics = system.collect()
        
        metrics_load = metrics['load']
        
        assert type(metrics_load['avg']['1']) == float
        assert type(metrics_load['avg']['5']) == float
        assert type(metrics_load['avg']['15']) == float
        
        metrics_cpu = metrics['cpu'][0] # hopefully at least 1 CPU! ;)
        
        assert type(metrics_cpu['idle']['/']) == float
        assert type(metrics_cpu['busy']['/']) == float
        assert type(metrics_cpu['busy']['user']['/']) == float
        assert type(metrics_cpu['busy']['system']['/']) == float
        
        metrics_memory = metrics['memory']
        
        try: # COMPAT: Python 2.7
            int_ish = [long, int]
        except NameError:
            int_ish = [int]
        
        assert type(metrics_memory['virtual']['b']) in int_ish
        assert type(metrics_memory['virtual']['avail']['b']) in int_ish
        assert type(metrics_memory['virtual']['avail']['/']) == float
        assert type(metrics_memory['virtual']['unavail']['b']) in int_ish
        assert type(metrics_memory['virtual']['unavail']['/']) == float
        assert type(metrics_memory['virtual']['used']['b']) in int_ish
        assert type(metrics_memory['virtual']['used']['/']) == float
        assert type(metrics_memory['virtual']['free']['b']) in int_ish
        assert type(metrics_memory['virtual']['free']['/']) == float
        assert type(metrics_memory['swap']['b']) in int_ish
        assert type(metrics_memory['swap']['used']['b']) in int_ish
        if '/' in metrics_memory['swap']['used']:
            assert type(metrics_memory['swap']['used']['/']) == float
        assert type(metrics_memory['swap']['free']['b']) in int_ish
        if '/' in metrics_memory['swap']['free']:
            assert type(metrics_memory['swap']['free']['/']) == float
        assert type(metrics_memory['swap']['sin']['b']) in int_ish
        assert type(metrics_memory['swap']['sout']['b']) in int_ish
        
        metrics_disk = metrics['disk']['/']
        
        assert type(metrics_disk['block_size']['b']) in int_ish
        assert type(metrics_disk['fragment_size']['b']) in int_ish
        assert type(metrics_disk['blocks']['n']) in int_ish
        assert type(metrics_disk['blocks']['free']['n']) in int_ish
        assert type(metrics_disk['blocks']['free']['/']) == float
        assert type(metrics_disk['blocks']['avail']['n']) in int_ish
        assert type(metrics_disk['blocks']['avail']['/']) == float
        assert type(metrics_disk['inodes']['n']) in int_ish
        assert type(metrics_disk['inodes']['free']['n']) in int_ish
        assert type(metrics_disk['inodes']['free']['/']) == float
        assert type(metrics_disk['inodes']['avail']['n']) in int_ish
        assert type(metrics_disk['inodes']['avail']['/']) == float
        assert type(metrics_disk['flags']) in int_ish
        assert type(metrics_disk['filename_len_max']) in int_ish
        assert type(metrics_disk['device']) == str
        assert type(metrics_disk['fstype']) == str
        assert type(metrics_disk['space']['b']) in int_ish
        assert type(metrics_disk['space']['used']['b']) in int_ish
        assert type(metrics_disk['space']['used']['/']) == float
        assert type(metrics_disk['space']['free']['b']) in int_ish
        assert type(metrics_disk['space']['free']['/']) == float
    
    def test_collect_mocked(self, monkeypatch):
        monkeypatch.setattr(os, 'getloadavg', self.mock_getloadavg)
        monkeypatch.setattr(os, 'statvfs', self.mock_statvfs)
        monkeypatch.setattr(psutil, 'cpu_times_percent',
                self.mock_cpu_times_percent)
        monkeypatch.setattr(psutil, 'virtual_memory',
                self.mock_virtual_memory)
        monkeypatch.setattr(psutil, 'swap_memory',
                self.mock_swap_memory)
        monkeypatch.setattr(psutil, 'disk_partitions',
                self.mock_disk_partitions)
        monkeypatch.setattr(psutil, 'disk_usage', self.mock_disk_usage)
        
        system = System({}, {})
        metrics = system.collect()
        
        # round floats (like beach balls)
        
        def round_dict(d):
            for k, v in d.items():
                if type(v) == dict:
                    d[k] = round_dict(v)
                elif k == '/':
                    d[k] = round(v, 2)
            return d
        
        round_dict(metrics['cpu'][0])
        round_dict(metrics['memory'])
        round_dict(metrics['disk']['/'])
        
        #
        
        assert metrics == {
            'load': {
                'avg': {
                    '1': 42.0,
                    '5': 84.0,
                    '15': 126.0}},
            'cpu': {
                0: {
                    'idle': {
                        '/': 0.55},
                    'busy': {
                        '/': 0.45,
                        'user': {
                            '/': 0.01},
                        'system': {
                            '/': 0.02},
                        'nice': {
                            '/': 0.03},
                        'iowait': {
                            '/': 0.04},
                        'irq': {
                            '/': 0.05},
                        'softirq': {
                            '/': 0.06},
                        'steal': {
                            '/': 0.07},
                        'guest': {
                            '/': 0.08},
                        'guest_nice': {
                            '/': 0.09}}}},
            'memory': {
                'virtual': {
                    'b': 8589934592,
                    'avail': {
                        'b': 4248592384,
                        '/': 0.49},
                    'unavail': {
                        'b': 4341342208,
                        '/': 0.51},
                    'used': {
                        'b': 4688113664,
                        '/': 0.55},
                    'free': {
                        'b': 3279757312,
                        '/': 0.38},
                    'active': {
                        'b': 2415570944,
                        '/': 0.28},
                    'inactive': {
                        'b': 968835072,
                        '/': 0.11},
                    'buffers': {
                        'b': 258020000,
                        '/': 0.03},
                    'cached': {
                        'b': 241716800,
                        '/': 0.03},
                    'wired': {
                        'b': 1303707648,
                        '/': 0.15},
                    'shared': {
                        'b': 50448000,
                        '/': 0.01}},
                'swap': {
                    'b': 2147483648,
                    'used': {
                        'b': 1196949504,
                        '/': 0.56},
                    'free': {
                        'b': 950534144,
                        '/': 0.44},
                    'sin': {
                        'b': 66084589568},
                    'sout': {
                        'b': 1213657088}}},
            'disk': {
                '/': {
                    'block_size': {
                        'b': 1764},
                    'fragment_size': {
                        'b': 1765},
                    'blocks': {
                        'n': 42,
                        'free': {
                            'n': 74088,
                            '/': 1764.0},
                        'avail': {
                            'n': 1768,
                            '/': 42.1}},
                    'inodes': {
                        'n': 1769,
                        'free': {
                            'n': 130691232,
                            '/': 73878.59},
                        'avail': {
                            'n': 3111696,
                            '/': 1759.01}},
                    'flags': 1772,
                    'filename_len_max': 1773,
                    'device': '/dev/disk42',
                    'fstype': 'zaphod',
                    'space': {
                        'b': 100440011101,
                        'used': {
                            'b': 1800538114,
                            '/': 0.02},
                        'free': {
                            'b': 98639472987,
                            '/': 0.98}}}}}
    
    def test_collect_swap_zero_total(self, monkeypatch):
        monkeypatch.setattr(os, 'getloadavg', self.mock_getloadavg)
        monkeypatch.setattr(os, 'statvfs', self.mock_statvfs)
        monkeypatch.setattr(psutil, 'cpu_times_percent',
                self.mock_cpu_times_percent)
        monkeypatch.setattr(psutil, 'virtual_memory',
                self.mock_virtual_memory)
        monkeypatch.setattr(psutil, 'swap_memory',
                self.mock_swap_memory_zero_total)
        monkeypatch.setattr(psutil, 'disk_partitions',
                self.mock_disk_partitions)
        monkeypatch.setattr(psutil, 'disk_usage', self.mock_disk_usage)
        
        system = System({}, {})
        metrics = system.collect()
    
    def test_collect_load_oserror(self, monkeypatch):
        def mock_getloadavg():
            raise OSError
        
        monkeypatch.setattr(os, 'getloadavg', mock_getloadavg)
        
        system = System({}, {})
        metrics = system.collect()
        
        assert metrics['load'] == {}
    
    def test_collect_disk_statvfs_filenotfounderror(self, monkeypatch):
        def mock_statvfs(mount):
            raise IOError
        
        monkeypatch.setattr(os, 'statvfs', mock_statvfs)
        
        system = System({}, {})
        metrics = system.collect()
        
        assert metrics['disk']['/'] == {}
    
    def test_collect_disk_disk_usage_oserror(self, monkeypatch):
        def mock_disk_usage(mount):
            raise OSError
        
        monkeypatch.setattr(psutil, 'disk_usage', mock_disk_usage)
        
        system = System({}, {})
        metrics = system.collect()
        
        assert metrics['disk']['/'] == {}
