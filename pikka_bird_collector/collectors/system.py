import os
import psutil

from pikka_bird_collector.collectors.base import Base


class System(Base):
    
    CPU_SAMPLE_S = 0.1
    
    def enabled(self):
        return True # always attempt to collect system metrics
    
    def collect(self):
        return ('system', {
            'load':   self.__load(),
            'cpu':    self.__cpu(),
            'memory': self.__memory(),
            'disk':   self.__disk()})
    
    def __load(self):
        try:
            load1, load5, load15 = os.getloadavg()
            
            return {
                '1_min_avg':  load1,
                '5_min_avg':  load5,
                '15_min_avg': load15}
        except OSError:
            return {}
    
    def __cpu(self):
        metrics = {}
        
        ctps = psutil.cpu_times_percent(self.CPU_SAMPLE_S, percpu=True)
        
        for cpu_i, ctp in enumerate(ctps):
            ctp_fs = ctp._fields
            
            metrics_cpu = {
                'idle_/':             ctp.idle,
                'busy_/':            (100 - ctp.idle),
                'busy_user_/':       ctp.user,
                'busy_system_/':     ctp.system,
                'busy_nice_/':       'nice' in ctp_fs       and ctp.nice,
                'busy_iowait_/':     'iowait' in ctp_fs     and ctp.iowait,
                'busy_irq_/':        'irq' in ctp_fs        and ctp.irq,
                'busy_softirq_/':    'softirq' in ctp_fs    and ctp.softirq,
                'busy_steal_/':      'steal' in ctp_fs      and ctp.steal,
                'busy_guest_/':      'guest' in ctp_fs      and ctp.guest,
                'busy_guest_nice_/': 'guest_nice' in ctp_fs and ctp.guest_nice}
            
            metrics[int(cpu_i)] = { k: v / 100 for k, v in metrics_cpu.items()
                    if v is not False } # filter metrics unavailable on system
        
        return metrics
    
    def __memory(self):
        metrics = {}
        
        virtual = psutil.virtual_memory()
        
        virtual_fs = virtual._fields
        
        virtual_unavailable = virtual.total - virtual.available
        
        metrics_virtual = {
            'virtual_b':             virtual.total,
            'virtual_available_b':   virtual.available,
            'virtual_available_/':   (virtual.available / virtual.total),
            'virtual_unavailable_b': virtual_unavailable,
            'virtual_unavailable_/': (virtual_unavailable / virtual.total),
            'virtual_used_b':        virtual.used,
            'virtual_used_/':        (virtual.used / virtual.total),
            'virtual_free_b':        virtual.free,
            'virtual_free_/':        (virtual.free / virtual.total),
            'virtual_active_b':
                'active' in virtual_fs   and virtual.active,
            'virtual_active_/':
                'active' in virtual_fs   and (virtual.active / virtual.total),
            'virtual_inactive_b':
                'inactive' in virtual_fs and virtual.inactive,
            'virtual_inactive_/':
                'inactive' in virtual_fs and (virtual.inactive / virtual.total),
            'virtual_buffers_b':
                'buffers' in virtual_fs  and virtual.buffers,
            'virtual_buffers_/':
                'buffers' in virtual_fs  and (virtual.buffers / virtual.total),
            'virtual_cached_b':
                'cached' in virtual_fs   and virtual.cached,
            'virtual_cached_/':
                'cached' in virtual_fs   and (virtual.cached / virtual.total),
            'virtual_wired_b':
                'wired' in virtual_fs    and virtual.wired,
            'virtual_wired_/':
                'wired' in virtual_fs    and (virtual.wired / virtual.total),
            'virtual_shared_b':
                'shared' in virtual_fs   and virtual.shared,
            'virtual_shared_/':
                'shared' in virtual_fs   and (virtual.shared / virtual.total)}
        
        metrics.update({ k: v for k, v in metrics_virtual.items()
                    if v is not False }) # filter metrics unavailable on system
        
        swap = psutil.swap_memory()
        
        metrics_swap = {
            'swap_b':      swap.total,
            'swap_used_b': swap.used,
            'swap_used_/': (swap.used / swap.total),
            'swap_free_b': swap.free,
            'swap_free_/': (swap.free / swap.total),
            'sin_b':       swap.sin,
            'sout_b':      swap.sout}
        
        metrics.update(metrics_swap)
        
        return metrics
    
    def __disk(self):
        metrics = {}
        
        partitions = [p for p in psutil.disk_partitions(all=False)]
        
        for partition in partitions:
            try:
                stats = os.statvfs(partition.mountpoint)
                usage = psutil.disk_usage(partition.mountpoint)
                
                metrics[partition.mountpoint] = {
                    'block_size_b':         stats.f_bsize,
                    'fragment_size_b':      stats.f_frsize,
                    'blocks':               stats.f_blocks,
                    'blocks_free':          stats.f_bfree,
                    'blocks_free_/':        (stats.f_bfree / stats.f_blocks),
                    'blocks_free_unpriv':   stats.f_bavail,
                    'blocks_free_unpriv_/': (stats.f_bavail / stats.f_blocks),
                    'inodes':               stats.f_files,
                    'inodes_free':          stats.f_ffree,
                    'inodes_free_/':        (stats.f_ffree / stats.f_files),
                    'inodes_free_unpriv':   stats.f_favail,
                    'inodes_free_unpriv_/': (stats.f_favail / stats.f_files),
                    'flags':                stats.f_flag,
                    'filename_len_max':     stats.f_namemax,
                    'device':               partition.device,
                    'fstype':               partition.fstype,
                    'space_b':              usage.total,
                    'space_used_b':         usage.used,
                    'space_used_/':         (usage.used / usage.total),
                    'space_free_b':         usage.free,
                    'space_free_/':         (usage.free / usage.total)}
            except (FileNotFoundError, OSError):
                metrics[partition.mountpoint] = {}
        
        return metrics
