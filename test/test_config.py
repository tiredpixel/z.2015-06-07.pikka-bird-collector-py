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
            '6379': None,
            '6380': {'password': 'PASSWORD'},
            '6381': {}}
        
        assert config.settings('mysterious-service') == {}
    
    def test_config_yaml(self):
        config = Config(TestConfig.fixture_path('config/config.yaml'))
        
        assert config.settings('redis') == {
            '6379': None,
            '6380': {'password': 'PASSWORD'},
            '6381': {}}
        
        assert config.settings('mysterious-service') == {}
    
    def test_config_conf_d(self):
        config = Config(TestConfig.fixture_path('config/conf.d'))
        
        assert config.settings('redis') == {
            '6342': None,
            '6379': None,
            '6380': {'password': 'PASSWORD'},
            '6381': {}}
        
        assert config.settings('mysql') == {
            '3306': None}
        
        assert config.settings('mysterious-service') == {}
