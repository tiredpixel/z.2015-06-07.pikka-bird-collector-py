from pikka_bird_collector.collectors.base import Base


class TestBase:
    
    def test_parse_str_setting_key(self):
      assert Base.parse_str_setting_key('SectionName ') == 'sectionname'
    
    def test_parse_str_setting_key_empty(self):
      assert Base.parse_str_setting_key('') == ''
    
    def test_parse_str_setting_value(self):
      assert Base.parse_str_setting_value('') is None
    
    def test_parse_str_setting_value_string(self):
      assert Base.parse_str_setting_value(' OK ') == 'OK'
    
    def test_parse_str_setting_value_integer(self):
      assert Base.parse_str_setting_value('42') == 42
    
    def test_parse_str_setting_value_decimal(self):
      assert Base.parse_str_setting_value('42.42') == 42.42
