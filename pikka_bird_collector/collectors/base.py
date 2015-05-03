class Base():
    """
        Base class, from which others inherit. Collector classes are passed the
        environment, in case they need to take OS-specific logic, etc. Classes
        should conform to the interface below.
        
        IMPLEMENT:
            collect()
        """
    
    @classmethod
    def service(cls):
        """
            Name of service the collector defines.
            """
        return cls.__name__.lower()
    
    def __init__(self, environment, settings):
        self.environment = environment
        self.settings    = settings or {}
    
    def enabled(self):
        """
            Whether this Collector is enabled for this run. Here, collectors can
            check whether services are installed, or relevant settings are
            present in the config, etc.
            
            RETURN:
                : boolean
                    whether this collector is enabled for this run
            """
        return len(self.settings) >= 1
    
    def collect(self):
        """
            Collect metrics for this run, returning both the service name and
            actual report. `collect()` is called for each Collector only once
            per run, so if there are multiple instances (e.g. multiple copies of
            MySQL running on different ports), Collectors should take this into
            account and include it as part of their data structure (e.g. with
            each set of metrics nested under the port).
            
            RETURN:
                : dict
                    metrics data, the structure of which the collector is free
                    to define for itself
            """
        pass # IMPLEMENT
    
    @staticmethod
    def parse_str_setting_key(key):
        return key.strip().lower()
    
    @staticmethod
    def parse_str_setting_value(value):
        v = value.strip()
        
        if v == '':
            return None
        
        try:
            v = int(v)
        except ValueError:
            try:
                v = float(v)
            except ValueError:
                pass
        
        return v
