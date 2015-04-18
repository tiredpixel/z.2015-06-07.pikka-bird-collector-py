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
    
    REQUEST_HEADER = {
        'Content-Type': 'application/json'}
    
    def __init__(self, server_uri, logger=None):
        self.server_uri = server_uri
        self.logger     = logger or logging.getLogger()
        
        self.__set_meta()
    
    def send(self, collection):
        self.logger.info("SENDING")
        
        collection.update(self.meta)
        
        r = requests.post(self.__service_url('collections'),
            data=json.dumps(collection),
            headers=self.REQUEST_HEADER)
        
        try:
            r.raise_for_status()
            l = self.logger.info
        except requests.exceptions.HTTPError:
            l = self.logger.error
        
        l("SENT %(s)s %(t)s" % { 's': r.status_code, 't': r.text })
    
    def __set_meta(self):
        self.meta = {
            'hostname': socket.gethostname(),
            'pid': os.getpid(),
            'version': pikka_bird_collector.__version__}
    
    def __service_url(self, service):
        service_path = self.SERVER_SERVICES[service]
        
        return urllib.parse.urljoin(self.server_uri, service_path)
