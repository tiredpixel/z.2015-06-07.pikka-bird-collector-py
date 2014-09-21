import os

from pikka_bird_collector.collectors.base import Base


class System(Base):
    
    def enabled(self):
        return True # always attempt to collect system metrics
    
    def collect(self):
        return {
            'system': {
                'load': self.__load(),
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
    
    def __disk(self):
        metrics = {}
        
        mounts = ['/']
        
        for mount in mounts:
            try:
                stats = os.statvfs(mount)
                
                metrics[mount] = {
                    'block_size':           stats.f_bsize,
                    'fragment_size':        stats.f_frsize,
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
                    'filename_len_max':     stats.f_namemax}
            except FileNotFoundError:
                metrics[mount] = {}
        
        return metrics
