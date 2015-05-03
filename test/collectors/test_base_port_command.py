import subprocess
import pytest

from pikka_bird_collector.collectors.base_port_command import BasePortCommand


class TestBasePortCommand:
    
    COMMAND_OK          = ['echo', 'HELLO']
    COMMAND_ERR_STATUS  = ['test', '-f', '__666__']
    COMMAND_ERR_MISSING = ['echoooooooooo']
    
    def test_exec_command(self):
        assert BasePortCommand.exec_command(self.COMMAND_OK) == 'HELLO\n'
    
    def test_exec_command_status(self):
        assert BasePortCommand.exec_command(self.COMMAND_ERR_STATUS) == None
    
    def test_exec_command_missing(self):
        assert BasePortCommand.exec_command(self.COMMAND_ERR_MISSING) == None
