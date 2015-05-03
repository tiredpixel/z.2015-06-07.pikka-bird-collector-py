import subprocess

from .base import Base


class BasePortCommand(Base):
    """
        Base class for collectors scoped by port, gathering metrics using
        external command-line tools. (e.g. MySQL, PostgreSQL, Redis)
        
        IMPLEMENT:
            command_tool()
            parse_output()
            collect_port()
        """
    
    @staticmethod
    def command_tool(port, settings, command):
        """
            Generate a command list, suitable for passing to +exec_command()+,
            from the port, optional additional settings, and command.
            
            PARAMETERS:
                port : string
                    port for service
                settings : (dict, None)
                    additional settings
                command : string
                    command to pass to command-line tool, e.g. MySQL
                        SHOW VARIABLES
            RETURN:
                : list
                    command in list synax, e.g.
                        ['redis-cli', '-p', '6379', 'INFO']
            """
        pass # IMPLEMENT
    
    @staticmethod
    def parse_output(output):
        """
            Parse output from external command-line tool, returning metrics.
            
            PARAMETERS:
                output : string
                    output to parse; note 'universal newlines' is used in
                    subprocess, guaranteeing +\n+ endings
            
            RETURN:
                : dict
                    parsed metrics
            """
        pass # IMPLEMENT
    
    def collect_port(self, port, settings):
        """
            Collect metrics within individual port scope.
            
            PARAMETERS:
                port : string
                    port for which to collect metrics
                settings : (dict, None)
                    additional settings
            RETURN:
                : dict
                    metrics for port
            """
        pass # IMPLEMENT
    
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
    def command_parse_output(cls, port, settings, command):
        command_f = cls.command_tool(port, settings, command)
        output    = BasePortCommand.exec_command(command_f)
        
        return cls.parse_output(output)
    
    def collect(self):
        metrics = {}
        
        return { port: self.collect_port(port, settings)
            for port, settings in self.settings.items() }
