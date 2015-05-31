class Base():
    """
        Base class, from which others inherit.
        
        IMPLEMENT:
            parse2()
        """
    
    def __init__(self,
            converter_key=lambda e: e,
            converter_value=lambda e: e):
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
                raw : str, None
                    raw string to be parsed, if any
            
            RETURN:
                : dict
                    parsed output
            """
        self.__reset()
        
        if raw is None:
            return {}
        
        return self.parse2(raw)
    
    def parse2(self, raw):
        """
            PARAMETERS:
                raw : str
                    raw string to be parsed
            
            RETURN:
                : dict
                    parsed output
            """
        pass # IMPLEMENT
    
    def __reset(self):
        self.ds = {}
