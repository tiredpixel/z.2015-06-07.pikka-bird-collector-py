import os
import psutil

from pikka_bird_collector.collectors.base import Base


class System(Base):
    """
        Collector for system metrics: load, CPU, memory, disk. This is always
        enabled for any collector. This collector follows one of the design
        principles of Pikka Bird, which is to collect as many metrics as are
        available, including with convenience calculations which would require
        knowledge of which metrics to subtract from which, etc. Many metrics are
        provided in both their raw form (containing unit within key) and as a
        ratio (`_/`), which are used in preference to percentages.
        """
    
    # accuracy to use for ratios (decimal places)
    RATIO_DP = 4
    
    # time to sample CPUs (s)
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
                '1_min_avg':  round(load1, self.RATIO_DP),
                '5_min_avg':  round(load5, self.RATIO_DP),
                '15_min_avg': round(load15, self.RATIO_DP)}
        except OSError:
            return {}
    
    def __cpu(self):
        metrics = {}
        
        ctps = psutil.cpu_times_percent(self.CPU_SAMPLE_S, percpu=True)
        
        for cpu_i, ctp in enumerate(ctps):
            ctp_fs = ctp._fields
            
            metrics_cpu = {
                'idle_/':        ctp.idle,
                'busy_/':        (100 - ctp.idle),
                'busy_user_/':   ctp.user,
                'busy_system_/': ctp.system}
            
            if 'nice' in ctp_fs:
                metrics_cpu.update({
                    'busy_nice_/': ctp.nice})
            if 'iowait' in ctp_fs:
                metrics_cpu.update({
                    'busy_iowait_/': ctp.iowait})
            if 'irq' in ctp_fs:
                metrics_cpu.update({
                    'busy_irq_/': ctp.irq})
            if 'softirq' in ctp_fs:
                metrics_cpu.update({
                    'busy_softirq_/': ctp.softirq})
            if 'steal' in ctp_fs:
                metrics_cpu.update({
                    'busy_steal_/': ctp.steal})
            if 'guest' in ctp_fs:
                metrics_cpu.update({
                    'busy_guest_/': ctp.guest})
            if 'guest_nice' in ctp_fs:
                metrics_cpu.update({
                    'busy_guest_nice_/': ctp.guest_nice})
            
            metrics[cpu_i] = {
                k: round(v / 100.0, self.RATIO_DP)
                    for k, v in metrics_cpu.items()
                    if v is not False } # filter metrics unavailable on system
        
        return metrics
    
    def __memory(self):
        metrics = {}
        
        virtual = psutil.virtual_memory()
        
        virtual_fs = virtual._fields
        
        virtual_unavailable = virtual.total - virtual.available
        
        virtual_total = float(virtual.total) # COMPAT: Python 2.7
        
        metrics_virtual = {
            'virtual_available_/':   round(virtual.available / virtual_total, self.RATIO_DP),
            'virtual_available_b':   virtual.available,
            'virtual_b':             virtual.total,
            'virtual_free_/':        round(virtual.free / virtual_total, self.RATIO_DP),
            'virtual_free_b':        virtual.free,
            'virtual_unavailable_/': round(virtual_unavailable / virtual_total, self.RATIO_DP),
            'virtual_unavailable_b': virtual_unavailable,
            'virtual_used_/':        round(virtual.used / virtual_total, self.RATIO_DP),
            'virtual_used_b':        virtual.used}
        
        if 'active' in virtual_fs:
            metrics_virtual.update({
                'virtual_active_/': round(virtual.active / virtual_total, self.RATIO_DP),
                'virtual_active_b': virtual.active})
        if 'buffers' in virtual_fs:
            metrics_virtual.update({
                'virtual_buffers_/': round(virtual.buffers / virtual_total, self.RATIO_DP),
                'virtual_buffers_b': virtual.buffers})
        if 'cached' in virtual_fs:
            metrics_virtual.update({
                'virtual_cached_/': round(virtual.cached / virtual_total, self.RATIO_DP),
                'virtual_cached_b': virtual.cached})
        if 'inactive' in virtual_fs:
            metrics_virtual.update({
                'virtual_inactive_/': round(virtual.inactive / virtual_total, self.RATIO_DP),
                'virtual_inactive_b': virtual.inactive})
        if 'shared' in virtual_fs:
            metrics_virtual.update({
                'virtual_shared_/': round(virtual.shared / virtual_total, self.RATIO_DP),
                'virtual_shared_b': virtual.shared})
        if 'wired' in virtual_fs:
            metrics_virtual.update({
                'virtual_wired_/': round(virtual.wired / virtual_total, self.RATIO_DP),
                'virtual_wired_b': virtual.wired})
        
        metrics.update({ k: v for k, v in metrics_virtual.items()
                    if v is not False }) # filter metrics unavailable on system
        
        swap = psutil.swap_memory()
        
        metrics_swap = {
            'sin_b':       swap.sin,
            'sout_b':      swap.sout,
            'swap_b':      swap.total,
            'swap_free_b': swap.free,
            'swap_used_b': swap.used}
        
        swap_total = float(swap.total) # COMPAT: Python 2.7
        
        if swap.total > 0:
            metrics_swap.update({
                'swap_free_/': round(swap.free / swap_total, self.RATIO_DP),
                'swap_used_/': round(swap.used / swap_total, self.RATIO_DP)})
        
        metrics.update(metrics_swap)
        
        return metrics
    
    def __disk(self):
        metrics = {}
        
        partitions = [p for p in psutil.disk_partitions(all=False)]
        
        for partition in partitions:
            try:
                stats = os.statvfs(partition.mountpoint)
                usage = psutil.disk_usage(partition.mountpoint)
                
                stats_f_blocks = float(stats.f_blocks) # COMPAT: Python 2.7
                stats_f_files  = float(stats.f_files) # COMPAT: Python 2.7
                usage_total    = float(usage.total) # COMPAT: Python 2.7
                
                metrics[partition.mountpoint] = {
                    'block_size_b':         stats.f_bsize,
                    'blocks':               stats.f_blocks,
                    'blocks_free':          stats.f_bfree,
                    'blocks_free_/':        round(stats.f_bfree / stats_f_blocks, self.RATIO_DP),
                    'blocks_free_unpriv':   stats.f_bavail,
                    'blocks_free_unpriv_/': round(stats.f_bavail / stats_f_blocks, self.RATIO_DP),
                    'device':               partition.device,
                    'filename_len_max':     stats.f_namemax,
                    'flags':                stats.f_flag,
                    'fragment_size_b':      stats.f_frsize,
                    'fstype':               partition.fstype,
                    'inodes':               stats.f_files,
                    'inodes_free':          stats.f_ffree,
                    'inodes_free_/':        round(stats.f_ffree / stats_f_files, self.RATIO_DP),
                    'inodes_free_unpriv':   stats.f_favail,
                    'inodes_free_unpriv_/': round(stats.f_favail / stats_f_files, self.RATIO_DP),
                    'space_b':              usage.total,
                    'space_free_/':         round(usage.free / usage_total, self.RATIO_DP),
                    'space_free_b':         usage.free,
                    'space_used_/':         round(usage.used / usage_total, self.RATIO_DP),
                    'space_used_b':         usage.used}
            except (IOError, OSError):
                metrics[partition.mountpoint] = {}
        
        return metrics
