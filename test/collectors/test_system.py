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
        system = System({})
        
        assert system.enabled() == True
    
    def test_collect_live(self):
        system = System({})
        service, metrics = system.collect()
        
        assert service == 'system'
        
        metrics_load = metrics['load']
        
        assert type(metrics_load['1_min_avg']) == float
        assert type(metrics_load['5_min_avg']) == float
        assert type(metrics_load['15_min_avg']) == float
        
        metrics_cpu = metrics['cpu'][0] # hopefully at least 1 CPU! ;)
        
        assert type(metrics_cpu['idle_/']) == float
        assert type(metrics_cpu['busy_/']) == float
        assert type(metrics_cpu['busy_user_/']) == float
        assert type(metrics_cpu['busy_system_/']) == float
        
        metrics_memory = metrics['memory']
        
        try: # COMPAT: Python 2.7
            int_ish = [long, int]
        except NameError:
            int_ish = [int]
        
        assert type(metrics_memory['virtual_b']) in int_ish
        assert type(metrics_memory['virtual_available_b']) in int_ish
        assert type(metrics_memory['virtual_available_/']) == float
        assert type(metrics_memory['virtual_unavailable_b']) in int_ish
        assert type(metrics_memory['virtual_unavailable_/']) == float
        assert type(metrics_memory['virtual_used_b']) in int_ish
        assert type(metrics_memory['virtual_used_/']) == float
        assert type(metrics_memory['virtual_free_b']) in int_ish
        assert type(metrics_memory['virtual_free_/']) == float
        assert type(metrics_memory['swap_b']) in int_ish
        assert type(metrics_memory['swap_used_b']) in int_ish
        if 'swap_used_/' in metrics_memory:
            assert type(metrics_memory['swap_used_/']) == float
        assert type(metrics_memory['swap_free_b']) in int_ish
        if 'swap_free_/' in metrics_memory:
            assert type(metrics_memory['swap_free_/']) == float
        assert type(metrics_memory['sin_b']) in int_ish
        assert type(metrics_memory['sout_b']) in int_ish
        
        metrics_disk = metrics['disk']['/']
        
        assert type(metrics_disk['block_size_b']) in int_ish
        assert type(metrics_disk['fragment_size_b']) in int_ish
        assert type(metrics_disk['blocks']) in int_ish
        assert type(metrics_disk['blocks_free']) in int_ish
        assert type(metrics_disk['blocks_free_/']) == float
        assert type(metrics_disk['blocks_free_unpriv']) in int_ish
        assert type(metrics_disk['blocks_free_unpriv_/']) == float
        assert type(metrics_disk['inodes']) in int_ish
        assert type(metrics_disk['inodes_free']) in int_ish
        assert type(metrics_disk['inodes_free_/']) == float
        assert type(metrics_disk['inodes_free_unpriv']) in int_ish
        assert type(metrics_disk['inodes_free_unpriv_/']) == float
        assert type(metrics_disk['flags']) in int_ish
        assert type(metrics_disk['filename_len_max']) in int_ish
        assert type(metrics_disk['device']) == str
        assert type(metrics_disk['fstype']) == str
        assert type(metrics_disk['space_b']) in int_ish
        assert type(metrics_disk['space_used_b']) in int_ish
        assert type(metrics_disk['space_used_/']) == float
        assert type(metrics_disk['space_free_b']) in int_ish
        assert type(metrics_disk['space_free_/']) == float
    
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
        
        system = System({})
        service, metrics = system.collect()
        
        assert service == 'system'
        
        # round floats (like beach balls)
        
        for metric in [
            'idle_/',
            'busy_/',
            'busy_user_/',
            'busy_system_/',
            'busy_nice_/',
            'busy_iowait_/',
            'busy_irq_/',
            'busy_softirq_/',
            'busy_steal_/',
            'busy_guest_/',
            'busy_guest_nice_/']:
            metrics['cpu'][0][metric] = round(
                    metrics['cpu'][0][metric], 2)
        
        for metric in [
            'virtual_available_/',
            'virtual_unavailable_/',
            'virtual_used_/',
            'virtual_free_/',
            'virtual_active_/',
            'virtual_inactive_/',
            'virtual_buffers_/',
            'virtual_cached_/',
            'virtual_wired_/',
            'virtual_shared_/',
            'swap_used_/',
            'swap_free_/']:
            metrics['memory'][metric] = round(
                    metrics['memory'][metric], 2)
        
        for metric in [
            'blocks_free_/',
            'blocks_free_unpriv_/',
            'inodes_free_/',
            'inodes_free_unpriv_/',
            'space_used_/',
            'space_free_/']:
            metrics['disk']['/'][metric] = round(
                    metrics['disk']['/'][metric], 2)
        
        #
        
        assert metrics == {
            'load': {
                '1_min_avg': 42.0,
                '5_min_avg': 84.0,
                '15_min_avg': 126.0},
            'cpu': {
                0: {
                    'idle_/': 0.55,
                    'busy_/': 0.45,
                    'busy_user_/': 0.01,
                    'busy_system_/': 0.02,
                    'busy_nice_/': 0.03,
                    'busy_iowait_/': 0.04,
                    'busy_irq_/': 0.05,
                    'busy_softirq_/': 0.06,
                    'busy_steal_/': 0.07,
                    'busy_guest_/': 0.08,
                    'busy_guest_nice_/': 0.09}},
            'memory': {
                'virtual_b': 8589934592,
                'virtual_available_b': 4248592384,
                'virtual_available_/': 0.49,
                'virtual_unavailable_b': 4341342208,
                'virtual_unavailable_/': 0.51,
                'virtual_used_b': 4688113664,
                'virtual_used_/': 0.55,
                'virtual_free_b': 3279757312,
                'virtual_free_/': 0.38,
                'virtual_active_b': 2415570944,
                'virtual_active_/': 0.28,
                'virtual_inactive_b': 968835072,
                'virtual_inactive_/': 0.11,
                'virtual_buffers_b': 258020000,
                'virtual_buffers_/': 0.03,
                'virtual_cached_b': 241716800,
                'virtual_cached_/': 0.03,
                'virtual_wired_b': 1303707648,
                'virtual_wired_/': 0.15,
                'virtual_shared_b': 50448000,
                'virtual_shared_/': 0.01,
                'swap_b': 2147483648,
                'swap_used_b': 1196949504,
                'swap_used_/': 0.56,
                'swap_free_b': 950534144,
                'swap_free_/': 0.44,
                'sin_b': 66084589568,
                'sout_b': 1213657088},
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
                    'space_free_/': 0.98}}}
    
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
        
        system = System({})
        service, metrics = system.collect()
        
        assert service == 'system'
    
    def test_collect_load_oserror(self, monkeypatch):
        def mock_getloadavg():
            raise OSError
        
        monkeypatch.setattr(os, 'getloadavg', mock_getloadavg)
        
        system = System({})
        service, metrics = system.collect()
        
        assert service == 'system'
        
        assert metrics['load'] == {}
    
    def test_collect_disk_statvfs_filenotfounderror(self, monkeypatch):
        def mock_statvfs(mount):
            raise IOError
        
        monkeypatch.setattr(os, 'statvfs', mock_statvfs)
        
        system = System({})
        service, metrics = system.collect()
        
        assert service == 'system'
        
        assert metrics['disk']['/'] == {}
    
    def test_collect_disk_disk_usage_oserror(self, monkeypatch):
        def mock_disk_usage(mount):
            raise OSError
        
        monkeypatch.setattr(psutil, 'disk_usage', mock_disk_usage)
        
        system = System({})
        service, metrics = system.collect()
        
        assert service == 'system'
        
        assert metrics['disk']['/'] == {}
