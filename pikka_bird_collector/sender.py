import datetime
import logging
import json
try: # COMPAT: Python 2.7
    import urllib.parse as urllib_parse
except ImportError:
    import urlparse as urllib_parse
import msgpack
import requests


class Sender():
    """
        Sender, for sending collected reports to the Server.
        """
    
    SERVER_SERVICES = {
        'collections': '/collections'}
    
    def __init__(self, server_uri, format='binary', logger=None):
        self.server_uri = server_uri
        self.format     = format
        self.logger     = logger or logging.getLogger()
    
    def send(self, collection):
        """
            Send collected reports to the Server, handling failures gracefully.
            If there is a network failure or the Server does not understand the
            collection, this is logged and returned as status, with no retry
            attempted.
            
            PARAMETERS:
                collection : dict
                    collection of reports, as supplied by `Collector.collect()`
            
            RETURN:
                : boolean
                    whether sending of metrics was successful
            """
        
        url  = self.__service_url('collections')
        headers, data = self.__pack_collection(collection)
        
        t_0 = datetime.datetime.utcnow()
        self.logger.info("SENDING %s %s (%d b)" % (url, self.format, len(data)))
        
        try:
            r = requests.post(url, data=data, headers=headers)
            r.raise_for_status()
            status = True
        except requests.exceptions.HTTPError:
            status = False
        except requests.exceptions.ConnectionError:
            self.logger.error("SERVER CONNECTION FAILED")
            return False
        
        logger = self.logger.info if status else self.logger.error
        
        try:
            text = r.text
        except ValueError:
            text = None
        
        t = datetime.datetime.utcnow()
        logger("SENT %d %s (%s s)" % (r.status_code, text, (t - t_0).seconds))
        
        return status
    
    def __service_url(self, service):
        service_path = self.SERVER_SERVICES[service]
        
        return urllib_parse.urljoin(self.server_uri, service_path)
    
    def __pack_collection(self, collection):
        if self.format == 'binary':
            headers = { 'Content-Type': 'application/octet-stream' }
            data    = msgpack.packb(collection)
        elif self.format == 'json':
            headers = { 'Content-Type': 'application/json' }
            data    = json.dumps(collection)
        
        return (headers, data)
