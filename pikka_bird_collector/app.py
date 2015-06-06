import random
import time

from .collector import Collector
from .sender import Sender


class App():
    """
        Main app.
        """
    
    def __init__(self, args, logger):
        self.eternal = args.eternal
        self.logger  = logger
        
        self.collector = Collector(
            config=args.conf,
            logger=logger)
        
        self.sender = Sender(args.server_uri,
            format=args.format,
            logger=logger)
    
    def run(self):
        self.running = True
        
        while self.running:
            try:
                self.__run_loop()
            except KeyboardInterrupt:
                self.running = False
    
    def __run_loop(self):
        collection = self.collector.collect()
        self.sender.send(collection)
        
        if self.eternal is None:
            self.running = False
        else:
            s = self.__calculate_eternal_sleep()
            self.logger.info("WATCHING Perfectly Normal Beasts (%d s)" % s)
            time.sleep(s)
    
    def __calculate_eternal_sleep(self):
        interval = self.eternal
        mid      = round(interval / 2)
        
        return random.randint(interval - mid, interval + mid)
