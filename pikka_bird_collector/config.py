import json
import os
import yaml


class Config():
    """
        Optional external config, used for collectors. Configs must have the
        correct extension.
        
        FORMATS:
            .json
                JSON config
            .yaml
                YAML config
            conf.d/
                directory containing multiple config files; it is permitted to
                split a single service across multiple files down 1 level
        """
    
    EXT_JSON = '.json'
    EXT_YAML = '.yaml'
    
    def __init__(self, path):
        """
            PARAMETERS:
                path : string
                    filename or directory of configs to parse
            """
        self.__settings = self.__parse_path(path) or {}
    
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
    
    def __parse_path(self, path):
        if path is None:
            return {}
        
        if os.path.isdir(path):
            settings = {}
            
            for f in os.listdir(path):
                path_f = os.path.join(path, f)
                ss = self.__parse_file(path_f)
                for k, v in ss.items():
                    settings[k] = settings.get(k) or {}
                    settings[k].update(v)
            
            return settings
        else:
            return self.__parse_file(path)
    
    def __parse_file(self, path):
        with open(path) as f_h:
            data = f_h.read()
        
        _name, ext = os.path.splitext(path)
        
        if ext == self.EXT_JSON:
            settings = json.loads(data)
        elif ext == self.EXT_YAML:
            settings = yaml.safe_load(data)
        
        return settings
