import os

from pikka_bird_collector.config import Config


class TestConfig:
    
    @staticmethod
    def fixture_path(filename):
        return os.path.join(os.path.dirname(__file__), 'fixtures', filename)
    
    def test_config(self):
        config = Config(None)
        
        assert config.settings('mysterious-service') == {}
    
    def test_config_json(self):
        config = Config(TestConfig.fixture_path('config/config.json'))
        
        assert config.settings('redis') == {
            '6379': {},
            '6381': None,
            '6380': {'password': 'PASSWORD'}}
        
        assert config.settings('mysterious-service') == {}
