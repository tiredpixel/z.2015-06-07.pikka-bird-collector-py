import re

from .base import Base


class Redis(Base):
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
    
    def parse2(self, raw):
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
