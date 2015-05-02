import subprocess
import pytest

from pikka_bird_collector.collectors.base import Base


class TestBase:
    
    COMMAND_OK          = ['echo', 'HELLO']
    COMMAND_ERR_STATUS  = ['test', '-f', '__666__']
    COMMAND_ERR_MISSING = ['echoooooooooo']
    
    def test_exec_command(self):
        assert Base.exec_command(self.COMMAND_OK) == 'HELLO\n'
    
    def test_exec_command_status(self):
        assert Base.exec_command(self.COMMAND_ERR_STATUS) == None
    
    def test_exec_command_missing(self):
        assert Base.exec_command(self.COMMAND_ERR_MISSING) == None
