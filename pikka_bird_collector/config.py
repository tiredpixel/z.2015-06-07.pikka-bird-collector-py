import json
import os
import yaml


class Config():
    """
        Optional external config, used for collectors.
        """
    
    EXT_JSON = '.json'
    EXT_YAML = '.yaml'
    
    def __init__(self, path):
        """
            PARAMETERS:
                path : string
                    filename of config to parse
            """
        self.__settings = self.__parse_file(path)
    
    def settings(self, service):
        """
            Extract settings from config, if exists.
            
            PARAMETERS:
                service : string
                    service for which to extract settings
            RETURN:
                : dict
                    settings, empty if none found
            """
        ss = self.__settings.get(service) or {}
        
        return { str(k): v for k, v in ss.items() }
    
    def __parse_file(self, path):
        settings = {}
        
        if path is None:
            return settings
        
        with open(path) as f_h:
            data = f_h.read()
        
        _name, ext = os.path.splitext(path)
        
        if ext == self.EXT_JSON:
            settings = json.loads(data)
        elif ext == self.EXT_YAML:
            settings = yaml.safe_load(data)
        
        return settings
