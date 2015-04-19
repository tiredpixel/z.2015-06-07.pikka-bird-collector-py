class Base():
    """
        Base class, from which others inherit. Collector classes are passed the
        environment, in case they need to take OS-specific logic, etc. Classes
        should conform to the interface below.
        """
    
    def __init__(self, environment):
        self.environment = environment
    
    def enabled(self):
        """
            Whether this Collector is enabled for this run. Here, collectors can
            check whether services are installed, or relevant settings are
            present in the config, etc.
            
            RETURN:
                : boolean
                    whether this collector is enabled for this run
            """
        pass
    
    def collect(self):
        """
            Collect metrics for this run, returning both the service name and
            actual report. `collect()` is called for each Collector only once
            per run, so if there are multiple instances (e.g. multiple copies of
            MySQL running on different ports), Collectors should take this into
            account and include it as part of their data structure (e.g. with
            each set of metrics nested under the port).
            
            RETURN:
                : tuple (string, dict)
                    (service, data)
            """
        pass
