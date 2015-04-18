import datetime
import logging
import importlib
import platform
import sys


COLLECTORS = [
   'system']

for c in COLLECTORS:
   importlib.import_module('pikka_bird_collector.collectors.' + c)


class Collector():
    
    def __init__(self, logger=None):
        self.environment = self.__environment()
        self.logger      = logger or logging.getLogger()
    
    def collect(self):
        collecting_at = datetime.datetime.now()
        self.logger.info("COLLECTING")
        
        reports = {}
        
        for collector_klass in self.__collector_klasses():
            collector = collector_klass(self.environment)
            
            if collector.enabled():
                self.logger.info("COLLECTING " + collector_klass.__name__)
                
                service, metrics = collector.collect()
                
                reports[service] = metrics
                
                self.logger.info("COLLECTED " + collector_klass.__name__ + " " + service + " " + str(metrics))
            else:
                self.logger.info("SKIPPED " + collector_klass.__name__)
        
        collected_at = datetime.datetime.now()
        self.logger.info("COLLECTED")
        
        return self.__format_collection(
            collecting_at=collecting_at,
            collected_at=collected_at,
            reports=reports)
    
    def __environment(self):
        return {
            'system':  platform.system(),
            'release': platform.release(),
            'version': platform.version()}
    
    def __collector_klasses(self):
        module_base = 'pikka_bird_collector.collectors.'
        
        return [getattr(sys.modules[module_base + c], c.title())
            for c in COLLECTORS]
    
    def __format_collection(self,
            collecting_at=None, collected_at=None, reports=None):
        return {
            'collecting_at': collecting_at.isoformat(),
            'collected_at': collected_at.isoformat(),
            'reports': reports}
