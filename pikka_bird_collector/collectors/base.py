import subprocess


class Base():
    """
        Base class, from which others inherit. Collector classes are passed the
        environment, in case they need to take OS-specific logic, etc. Classes
        should conform to the interface below.
        """
    
    @staticmethod
    def exec_command(command):
        """
            Execute a system command using subprocess, returning the output. For
            any reasonable error, such as exit codes, the error is suppressed
            and +None+ is returned.
            
            PARAMETERS:
                command : list
                    command in list syntax, e.g.
                        ['redis-cli', '-p', '6379', 'INFO']
            RETURN:
                : string
                    output of command including both STDOUT and STDERR
                : None
                    command failed for some reason
            """
        try:
            return subprocess.check_output(command,
                stderr=subprocess.STDOUT,
                universal_newlines=True)
        except (IOError, OSError, subprocess.CalledProcessError):
            return
    
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
        return True
    
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
        return {}
