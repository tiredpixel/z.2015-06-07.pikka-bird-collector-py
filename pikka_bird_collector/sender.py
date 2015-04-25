import datetime
import logging
import json
try: # COMPAT: Python 2.7
    import urllib.parse as urllib_parse
except ImportError:
    import urlparse as urllib_parse
import requests


class Sender():
    """
        Sender, for sending collected reports to the Server.
        """
    
    SERVER_SERVICES = {
        'collections': '/collections'}
    
    REQUEST_HEADERS = {
        'Content-Type': 'application/json'}
    
    def __init__(self, server_uri, logger=None):
        self.server_uri = server_uri
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
        data = json.dumps(collection)
        
        t_0 = datetime.datetime.utcnow()
        self.logger.info("SENDING %s (%d b)" % (url, (len(data.encode('utf-8')))))
        
        try:
            r = requests.post(url, data=data, headers=self.REQUEST_HEADERS)
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
