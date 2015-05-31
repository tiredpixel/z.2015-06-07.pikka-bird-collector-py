import json
import re

from .base import Base


class Erlang(Base):
    """
        Parses simple Erlang data format, as output by RabbitMQ status.
        
        e.g.
            [{pid,296},
             {running_applications,
                 [{rabbitmq_management_visualiser,"RabbitMQ Visualiser","3.5.1"}]}]
        """
    
    RE_STRINGY = [re.compile(r'<<"(.*)">>'), r'"\g<1>"']
    
    CONTEXT_STRUCTURE = 0
    CONTEXT_KEY       = 1
    CONTEXT_VALUE     = 2
    
    CHAR_ARR_S = '{'
    CHAR_ARR_E = '}'
    CHAR_OBJ_S = '['
    CHAR_OBJ_E = ']'
    CHAR_QUOTE = '"'
    CHAR_SEP   = ','
    CHAR_WSP   = [' ', '\n']
    CHAR_E     = [CHAR_ARR_E, CHAR_OBJ_E]
    CHAR_SKIP  = CHAR_WSP + [CHAR_ARR_E]
    
    @staticmethod
    def dict_set(d, k, v):
        """
            Set value within arbitrary-depth dict, referenced by key path.
            
            Note this uses simple recursion, and will blow the stack if too
            deep.
            
            PARAMETERS:
                d : dict
                    dict to update
                k : list
                    reverse-ordered key (e.g. ['depth-3', 'depth-2', 'depth-1'])
                v : type
                    value to set
            """
        if len(k) == 1:
            d[k[0]] = v
        else:
            k2 = k.pop()
            if k2 not in d:
                d[k2] = {}
            Erlang.dict_set(d[k2], k, v)
    
    def parse2(self, raw):
        self.__reset(raw)
        
        parse_contexts = {
            Erlang.CONTEXT_STRUCTURE: self.__parse_structure,
            Erlang.CONTEXT_KEY:       self.__parse_key,
            Erlang.CONTEXT_VALUE:     self.__parse_value}
        
        while self.r_i < len(self.raw):
            parse_contexts[self.r_context]()
            self.r_i += 1
        
        return self.ds
    
    def __parse_structure(self):
        c = self.__read_skip()
        
        if c == Erlang.CHAR_OBJ_S and self.__read_lookahead_structure():
            self.r_i += 1
        
        self.r_context = Erlang.CONTEXT_KEY
    
    def __parse_key(self):
        c = self.__read_char(self.r_i)
        
        if c == Erlang.CHAR_SEP:
            if self.e_context_p == Erlang.CONTEXT_KEY:
                self.r_depth += 1 # dive, dive!
            
            self.__emit_key()
            self.r_context = Erlang.CONTEXT_VALUE
        else:
            self.r_buffer += c
    
    def __parse_value(self):
        c = self.__read_char(self.r_i)
        
        if c == Erlang.CHAR_QUOTE:
            self.r_quoted *= -1 # toggle
        
        if self.r_quoted == -1 and c in Erlang.CHAR_E:
            if self.e_context_p == Erlang.CONTEXT_KEY:
                self.__emit_value()
            
            self.r_i += 1
            c = self.__read_skip()
            
            if c == Erlang.CHAR_SEP:
                self.r_context = Erlang.CONTEXT_STRUCTURE
            elif c == Erlang.CHAR_OBJ_E:
                self.r_depth -= 1 # going up!
        elif self.r_quoted == -1 and c == Erlang.CHAR_OBJ_S:
            if self.__read_lookahead_structure():
                self.r_context = Erlang.CONTEXT_STRUCTURE
        elif self.r_quoted == 1 or c != Erlang.CHAR_ARR_S:
            self.r_buffer += c
    
    def __reset(self, raw):
        self.raw = raw
        
        self.r_i       = 0 # read pointer
        self.r_context = Erlang.CONTEXT_STRUCTURE # type of data
        self.r_buffer  = '' # buffer for data
        self.r_depth   = 0 # depth within structure
        self.r_quoted  = -1 # within quotes? t: 1, f: -1
        
        self.e_context_p = None # previous type of data
        self.e_buffer    = [] # buffer for data
        self.e_key       = [] # full path of key
    
    def __read_char(self, i):
        if i < len(self.raw):
            return self.raw[i]
    
    def __read_skip(self):
        c = self.__read_char(self.r_i)
        
        while c in Erlang.CHAR_SKIP:
            self.r_i += 1
            c = self.__read_char(self.r_i)
        
        return c
    
    def __read_lookahead_structure(self):
        r_i_0 = self.r_i
        
        self.r_i += 1
        c = self.__read_skip()
        
        if c == Erlang.CHAR_ARR_S:
            status = True
        else:
            status = False
        
        self.r_i = r_i_0
        return status
    
    def __emit_key(self):
        k = self.r_buffer.strip() # hacky strip
        k = self.converter_key(k)
        
        if len(self.e_key) > self.r_depth:
            self.e_key[self.r_depth] = k
        else:
            self.e_key.append(k)
        
        self.e_buffer = [k]
        self.e_key    = self.e_key[:(self.r_depth + 1)]
        
        self.e_context_p = Erlang.CONTEXT_KEY
        self.r_buffer = ''
    
    def __emit_value(self):
        v = Erlang.__parse_str_setting_value(self.r_buffer)
        v = self.converter_value(v)
        
        self.e_buffer.append(v)
        Erlang.dict_set(self.ds, self.e_key[::-1], v)
        
        self.e_context_p = Erlang.CONTEXT_VALUE
        self.r_buffer = ''
    
    @staticmethod
    def __parse_str_setting_value(v):
        v = Erlang.RE_STRINGY[0].sub(Erlang.RE_STRINGY[1], v)
        
        try:
            v = json.loads('[' + v + ']')
        except ValueError:
            v = v.split(Erlang.CHAR_SEP)
        
        if len(v) == 0:
            v = None
        elif len(v) == 1:
            v = v[0]
        
        return v
