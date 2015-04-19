import datetime
import importlib
import logging
import os
import platform
import socket
import sys

import pikka_bird_collector


COLLECTORS = [
   'system']

for c in COLLECTORS:
   importlib.import_module('pikka_bird_collector.collectors.' + c)


class Collector():
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger()
        
        self.__set_environment()
    
    def collect(self):
        reports = {}
        
        collecting_at = datetime.datetime.utcnow()
        self.logger.info("COLLECTING")
        
        for collector_klass in self.__collector_klasses():
            collector = collector_klass(self.environment)
            name      = collector_klass.__name__
            
            if collector.enabled():
                self.logger.info("COLLECTING %s" % name)
                
                service, metrics = collector.collect()
                
                reports[service] = metrics
                
                self.logger.debug("METRICS %s %s" % (service, metrics))
            else:
                self.logger.info("SKIPPED %s" % name)
        
        collected_at = datetime.datetime.utcnow()
        self.logger.info("COLLECTED (%d s)" % (collected_at - collecting_at).seconds)
        
        return {
            'collecting_at': collecting_at.isoformat(),
            'collected_at':  collected_at.isoformat(),
            'environment':   self.environment,
            'reports':       reports}
    
    def __set_environment(self):
        self.environment = {
            'hostname': socket.gethostname(),
            'pid':      os.getpid(),
            'version':  pikka_bird_collector.__version__,
            'platform': {
                'system':  platform.system(),
                'release': platform.release(),
                'version': platform.version()}}
        
        self.logger.info("ENVIRONMENT %s" % self.environment)
    
    def __collector_klasses(self):
        module_base = 'pikka_bird_collector.collectors.'
        
        return [getattr(sys.modules[module_base + c], c.title())
            for c in COLLECTORS]
