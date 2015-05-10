def table(output,
        delim_row='\n',
        delim_col='\t',
        converter_key=None,
        converter_value=None,
        transpose=False,
        tag_header_col=None):
    """
        Parses common table formats.
        
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
            tag_header_col : string
                read multiple columns per row, matched to header, with each row
                tagged by unique key referenced from header
                
                e.g.
                    KEY0,KEY1,KEY2_PK
                    VALUE0,VALUE1,VALUE2
                    
                    {
                        KEY2_PK: {
                            KEY0:    VALUE0,
                            KEY1:    VALUE1,
                            KEY2_PK: VALUE2}}
        
        RETURN:
            : dict
                parsed output, in format above
        """
    if output is None:
        return {}
    
    ds = {}
    
    rows   = [ r.split(delim_col) for r in output.split(delim_row) ]
    header = [ converter_key(k) for k in rows[0] ]
    
    for row in rows[1:]:
        if len(row) == len(header):
            if transpose:
                for i, v in enumerate(row):
                    k = converter_key(header[i])
                    ds[k] = converter_value(v)
            else:
                if tag_header_col:
                    h_i = header.index(tag_header_col)
                    k = converter_key(row[h_i])
                    ds[k] = {}
                    for i, v in enumerate(row):
                        ds[k][header[i]] = converter_value(v)
                else:
                    k = converter_key(row[0])
                    ds[k] = converter_value(row[1])
    
    return ds
