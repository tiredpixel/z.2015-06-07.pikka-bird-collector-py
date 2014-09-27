import os
import psutil

from pikka_bird_collector.collectors.base import Base


class System(Base):
    
    def enabled(self):
        return True # always attempt to collect system metrics
    
    def collect(self):
        return {
            'system': {
                'load': self.__load(),
                'cpu':  self.__cpu(),
                'disk': self.__disk()}}
    
    def __load(self):
        try:
            load1, load5, load15 = os.getloadavg()
            
            return {
                'avg_1_min':  load1,
                'avg_5_min':  load5,
                'avg_15_min': load15}
        except OSError:
            return {}
    
    def __cpu(self):
        metrics = {}
        
        ctps = psutil.cpu_times_percent(0.5, percpu=True) # sample 0.5 s
        
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
            
            metrics[cpu_i] = { k: v / 100 for k, v in metrics_cpu.items()
                    if v is not False } # filter metrics unavailable on system
        
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
