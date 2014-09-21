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
        self.logger.info("COLLECTING")
        
        for collector_klass in self.__collector_klasses():
            collector = collector_klass(self.environment)
            
            if collector.enabled():
                self.logger.info("COLLECTING " + collector_klass.__name__)
                
                metrics = collector.collect()
                
                self.logger.info("COLLECTED " + collector_klass.__name__ + " " + str(metrics))
            else:
                self.logger.info("SKIPPED " + collector_klass.__name__)
        
        self.logger.info("COLLECTED")
    
    def __environment(self):
        return {
            'system':  platform.system(),
            'release': platform.release(),
            'version': platform.version()}
    
    def __collector_klasses(self):
        module_base = 'pikka_bird_collector.collectors.'
        
        return [getattr(sys.modules[module_base + c], c.title())
            for c in COLLECTORS]
