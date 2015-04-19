import datetime
import logging
import json
import os
import socket
import urllib.parse
import requests

import pikka_bird_collector


class Sender():
    
    SERVER_SERVICES = {
        'collections': '/collections'}
    
    REQUEST_HEADERS = {
        'Content-Type': 'application/json'}
    
    def __init__(self, server_uri, logger=None):
        self.server_uri = server_uri
        self.logger     = logger or logging.getLogger()
        
        self.__set_process()
    
    def send(self, collection):
        url = self.__service_url('collections')
        collection.update(self.process)
        data = json.dumps(collection)
        
        t_0 = datetime.datetime.utcnow()
        self.logger.info("SENDING %s (%d b)" % (url, (len(data.encode('utf-8')))))
        
        try:
            r = requests.post(url, data=data, headers=self.REQUEST_HEADERS)
            r.raise_for_status()
            logger = self.logger.info
        except requests.exceptions.HTTPError:
            logger = self.logger.error
        
        t = datetime.datetime.utcnow()
        logger("SENT %d %s (%s s)" % (r.status_code, r.text, (t - t_0).seconds))
    
    def __set_process(self):
        self.process = {
            'hostname': socket.gethostname(),
            'pid':      os.getpid(),
            'version':  pikka_bird_collector.__version__}
        
        self.logger.info("PROCESS %s" % self.process)
    
    def __service_url(self, service):
        service_path = self.SERVER_SERVICES[service]
        
        return urllib.parse.urljoin(self.server_uri, service_path)
