import json
import os


class Config():
    """
        Optional external config file.
        """
    
    EXT_JSON = '.json'
    
    def __init__(self, path):
        self.settings = self.__parse_file(path)
    
    def __parse_file(self, path):
        settings = {}
        
        if path is None:
            return settings
        
        with open(path) as f_h:
            data = f_h.read()
        
        _name, ext = os.path.splitext(path)
        
        if ext == self.EXT_JSON:
            settings = json.loads(data)
        
        return settings
