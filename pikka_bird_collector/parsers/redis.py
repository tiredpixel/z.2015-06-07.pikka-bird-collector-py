import re


class Redis():
    """
        Parses main Redis INFO-type format.
        
        e.g.
            # Clients
            connected_clients:8
            client_longest_raw_list:0
            client_biggest_input_buf:0
            blocked_clients:0
        """
    
    RE_SECTION = re.compile(r'# (?P<section>.+)')
    RE_SETTING = re.compile(r'(?P<k>\w+):(?P<v>.*)')
    
    def __init__(self,
            converter_key=None,
            converter_value=None):
        """
            PARAMETERS:
                converter_key : function
                    function for converting keys
                    
                    e.g.
                        def converter_key(key):
                            return key.strip()
                converter_value : function
                    function for converting values
                    
                    e.g.
                        def converter_value(value):
                            return value.strip()
            """
        self.converter_key   = converter_key
        self.converter_value = converter_value
    
    def parse(self, raw):
        """
            PARAMETERS:
                raw : string
                    raw string to be parsed
            
            RETURN:
                : dict
                    parsed output
            """
        if raw is None:
            return {}
        
        self.__reset()
        
        section = None
        for row in raw.split('\n'):
            m_section = Redis.RE_SECTION.match(row)
            if m_section:
                section = self.converter_key(m_section.group('section'))
                self.ds[section] = {}
            else:
                m_setting = Redis.RE_SETTING.match(row)
                if m_setting:
                    k = self.converter_key(m_setting.group('k'))
                    v = self.converter_value(m_setting.group('v'))
                    if section is None:
                        self.ds[k] = v
                    else:
                        self.ds[section][k] = v
        
        return self.ds
    
    def __reset(self):
        self.ds = {}
