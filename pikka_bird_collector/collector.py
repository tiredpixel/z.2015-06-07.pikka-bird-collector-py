import datetime
import importlib
import logging
import os
import platform
import socket
import sys

import pikka_bird_collector
from .config import Config


COLLECTORS = [
    'system', # keep first; sort rest
    'mongodb',
    'mysql',
    'postgresql',
    'rabbitmq',
    'redis']

COLLECTORS_MODULE_P = 'pikka_bird_collector.collectors.'

for c in COLLECTORS:
   importlib.import_module(COLLECTORS_MODULE_P + c)


class Collector():
    """
        Main collector, which calls individual service Collectors and merges the
        results. The environment, containing such things as PID, hostname, and
        kernel version, are passed to each collector.
        """
    
    def __init__(self, config=None, logger=None):
        """
            PARAMETERS:
                path : string
                    filename of config to parse
                logger : logger
                    logger
            """
        self.config = Config(config)
        self.logger = logger or logging.getLogger()
        
        self.__set_environment()
    
    def collect(self):
        """
            Collect metrics for all invididual service Collectors, returning the
            reports in a format suitable for sending to the Server, complete
            with dates converted to strings. All times are in UTC, always.
            
            RETURN:
                : dict
                    collected reports, ready for sending to the Server
            """
        
        reports = {}
        
        collecting_at = datetime.datetime.utcnow()
        self.logger.info("COLLECTING")
        
        for c in COLLECTORS:
            klass = getattr(sys.modules[COLLECTORS_MODULE_P + c], c.title())
            
            service   = klass.service()
            collector = klass(self.environment, self.config.settings(service))
            
            if collector.enabled():
                self.logger.info("COLLECTING %s" % service)
                
                reports[service] = collector.collect()
                
                self.logger.debug("METRICS %s %s" % (service, reports[service]))
            else:
                self.logger.debug("SKIPPED %s" % service)
        
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
