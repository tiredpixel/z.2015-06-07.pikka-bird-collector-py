import os
import psutil

from .base import Base


class System(Base):
    """
        Collector for system.
        
        This collector is always enabled, and you can't disable it. This is
        intentional, as I can't think of a reason why you'd want to collect
        metrics from a server without caring about its health. :) This also
        enables Pikka Bird to be useful out the box; even with no configuration,
        it should at least start monitoring useful things.
        
        Every type of metric within this collector is always gathered.
        
        This collector gathers metrics for:
        
        - load average
        - CPU usage
        - memory usage
        - disk usage
        
        DEPENDENCIES:
            None
        
        SETTINGS:
            minimal:
                None
            supported:
                None
        """
    
    # accuracy to use for ratios (decimal places)
    RATIO_DP = 4
    
    # time to sample CPUs (s)
    CPU_SAMPLE_S = 0.1
    
    def enabled(self):
        return True
    
    def collect(self):
        return {
            'load':   self.__load(),
            'cpu':    self.__cpu(),
            'memory': self.__memory(),
            'disk':   self.__disk()}
    
    def __load(self):
        l_round = lambda e: round(e, self.RATIO_DP)
        
        try:
            load1, load5, load15 = os.getloadavg()
            
            return {
                'avg': {
                     '1': l_round(load1),
                     '5': l_round(load5),
                    '15': l_round(load15)}}
        except OSError:
            return {}
    
    def __cpu(self):
        metrics = {}
        
        ctps = psutil.cpu_times_percent(self.CPU_SAMPLE_S, percpu=True)
        
        l_round = lambda e: round(e / 100.0, self.RATIO_DP)
        
        for cpu_i, ctp in enumerate(ctps):
            ctp_fs = ctp._fields
            
            metrics_cpu = {
                'idle': {
                    '/': l_round(ctp.idle)},
                'busy': {
                    '/': l_round(100 - ctp.idle),
                    'user': {
                        '/': l_round(ctp.user)},
                    'system': {
                        '/': l_round(ctp.system)}}}
            
            if 'nice' in ctp_fs and ctp.nice:
                metrics_cpu['busy']['nice'] = {
                    '/': l_round(ctp.nice)}
            if 'iowait' in ctp_fs and ctp.iowait:
                metrics_cpu['busy']['iowait'] = {
                    '/': l_round(ctp.iowait)}
            if 'irq' in ctp_fs and ctp.irq:
                metrics_cpu['busy']['irq'] = {
                    '/': l_round(ctp.irq)}
            if 'softirq' in ctp_fs and ctp.softirq:
                metrics_cpu['busy']['softirq'] = {
                    '/': l_round(ctp.softirq)}
            if 'steal' in ctp_fs and ctp.steal:
                metrics_cpu['busy']['steal'] = {
                    '/': l_round(ctp.steal)}
            if 'guest' in ctp_fs and ctp.guest:
                metrics_cpu['busy']['guest'] = {
                    '/': l_round(ctp.guest)}
            if 'guest_nice' in ctp_fs and ctp.guest_nice:
                metrics_cpu['busy']['guest_nice'] = {
                    '/': l_round(ctp.guest_nice)}
            
            metrics[cpu_i] = metrics_cpu
        
        return metrics
    
    def __memory(self):
        metrics = {}
        
        virtual    = psutil.virtual_memory()
        virtual_fs = virtual._fields
        
        virtual_unavail = virtual.total - virtual.available
        
        virtual_total = float(virtual.total) # COMPAT: Python 2.7
        
        l_round = lambda e: round(e / virtual_total, self.RATIO_DP)
        
        metrics_virtual = {
            'b': virtual.total,
            'avail': {
                'b': virtual.available,
                '/': l_round(virtual.available)},
            'used': {
                'b': virtual.used,
                '/': l_round(virtual.used)},
            'free': {
                'b': virtual.free,
                '/': l_round(virtual.free)},
            'unavail': {
                'b': virtual_unavail,
                '/': l_round(virtual_unavail)}}
        
        if 'active' in virtual_fs and virtual.active:
            metrics_virtual['active'] = {
                'b': virtual.active,
                '/': l_round(virtual.active)}
        if 'inactive' in virtual_fs and virtual.inactive:
            metrics_virtual['inactive'] = {
                'b': virtual.inactive,
                '/': l_round(virtual.inactive)}
        if 'buffers' in virtual_fs and virtual.buffers:
            metrics_virtual['buffers'] = {
                'b': virtual.buffers,
                '/': l_round(virtual.buffers)}
        if 'cached' in virtual_fs and virtual.cached:
            metrics_virtual['cached'] = {
                'b': virtual.cached,
                '/': l_round(virtual.cached)}
        if 'wired' in virtual_fs and virtual.wired:
            metrics_virtual['wired'] = {
                'b': virtual.wired,
                '/': l_round(virtual.wired)}
        if 'shared' in virtual_fs and virtual.shared:
            metrics_virtual['shared'] = {
                'b': virtual.shared,
                '/': l_round(virtual.shared)}
        
        metrics['virtual'] = metrics_virtual
        
        swap = psutil.swap_memory()
        
        metrics_swap = {
            'b': swap.total,
            'used': {
                'b': swap.used},
            'free': {
                'b': swap.free},
            'sin': {
                'b': swap.sin},
            'sout': {
                'b': swap.sout}}
        
        swap_total = float(swap.total) # COMPAT: Python 2.7
        
        if swap.total > 0:
            metrics_swap['free']['/'] = round(swap.free / swap_total, self.RATIO_DP)
            metrics_swap['used']['/'] = round(swap.used / swap_total, self.RATIO_DP)
        
        metrics['swap'] = metrics_swap
        
        return metrics
    
    def __disk(self):
        metrics = {}
        
        partitions = [p for p in psutil.disk_partitions(all=False)]
        
        l_round = lambda e, f: round(e / f, self.RATIO_DP)
        
        for partition in partitions:
            try:
                stats = os.statvfs(partition.mountpoint)
                usage = psutil.disk_usage(partition.mountpoint)
                
                stats_f_blocks = float(stats.f_blocks) # COMPAT: Python 2.7
                stats_f_files  = float(stats.f_files) # COMPAT: Python 2.7
                usage_total    = float(usage.total) # COMPAT: Python 2.7
                
                metrics[partition.mountpoint] = {
                    'block_size': {
                        'b': stats.f_bsize},
                    'blocks': {
                        'n': stats.f_blocks,
                        'free': {
                            'n': stats.f_bfree,
                            '/': l_round(stats.f_bfree, stats_f_blocks)},
                        'avail': {
                            'n': stats.f_bavail,
                            '/': l_round(stats.f_bavail, stats_f_blocks)}},
                    'device': partition.device,
                    'filename_len_max': stats.f_namemax,
                    'flags': stats.f_flag,
                    'fragment_size': {
                        'b': stats.f_frsize},
                    'fstype': partition.fstype,
                    'inodes': {
                        'n': stats.f_files,
                        'free': {
                            'n': stats.f_ffree,
                            '/': l_round(stats.f_ffree, stats_f_files)},
                        'avail': {
                            'n': stats.f_favail,
                            '/': l_round(stats.f_favail, stats_f_files)}},
                    'space': {
                        'b': usage.total,
                        'free': {
                            'b': usage.free,
                            '/': l_round(usage.free, usage_total)},
                        'used': {
                            'b': usage.used,
                            '/': l_round(usage.used, usage_total)}}}
            except (IOError, OSError):
                metrics[partition.mountpoint] = {}
        
        return metrics
