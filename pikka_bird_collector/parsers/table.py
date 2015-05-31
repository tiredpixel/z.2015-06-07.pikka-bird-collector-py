from .base import Base


class Table(Base):
    """
        Parses common table formats.
        
        e.g. non-transpose
            header-key|header-value
            KEY0|VALUE0
            KEY1|VALUE1
            KEY2|VALUE2
            
            {
                KEY0: VALUE0,
                KEY1: VALUE1,
                KEY2: VALUE2}
        
        e.g. transpose
            KEY0|KEY1|KEY2
            VALUE0|VALUE1|VALUE2
            
            {
                KEY0: VALUE0,
                KEY1: VALUE1,
                KEY2: VALUE2}
        
        e.g. tag_header_col
            KEY0,KEY1,KEY2_PK
            VALUE0,VALUE1,VALUE2
            
            {
                KEY2_PK: {
                    KEY0:    VALUE0,
                    KEY1:    VALUE1,
                    KEY2_PK: VALUE2}}
        """
    
    def __init__(self,
            delim_row='\n',
            delim_col='\t',
            converter_key=None,
            converter_value=None,
            transpose=False,
            tag_header_col=None):
        """
            PARAMETERS:
                delim_row : string
                    row delimiter character
                delim_col : string
                    column delimiter character
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
                transpose : boolean
                    transpose mode, where keys are header, and values are single
                    row; otherwise, keys are column 0, and values are column 1, with
                    header required but ignored
                tag_header_col : string
                    (only supported for non-transpose)
                    read multiple columns per row, matched to header, with each row
                    tagged by unique key referenced from header
            """
        self.delim_row = delim_row
        self.delim_col = delim_col
        
        self.converter_key   = converter_key
        self.converter_value = converter_value
        
        self.transpose = transpose
        if not transpose:
            self.tag_header_col = tag_header_col
    
    def parse2(self, raw):
        rows   = [ r.split(self.delim_col) for r in raw.split(self.delim_row) ]
        header = [ self.converter_key(k) for k in rows[0] ]
        
        for row in rows[1:]:
            if len(row) == len(header):
                if self.transpose:
                    self.__parse_row_transpose(row, header)
                else:
                    if self.tag_header_col:
                        self.__parse_row_tag_header_col(row, header)
                    else:
                        self.__parse_row_non_transpose(row)
        
        return self.ds
    
    def __parse_row_non_transpose(self, row):
        k = self.converter_key(row[0])
        self.ds[k] = self.converter_value(row[1])
    
    def __parse_row_transpose(self, row, header):
        for i, v in enumerate(row):
            k = self.converter_key(header[i])
            self.ds[k] = self.converter_value(v)
    
    def __parse_row_tag_header_col(self, row, header):
        h_i = header.index(self.tag_header_col)
        k = self.converter_key(row[h_i])
        self.ds[k] = {}
        
        for i, v in enumerate(row):
            self.ds[k][header[i]] = self.converter_value(v)
