def parse_cookie(header):
    """
    Parse a Cookie header string into a dictionary.
    
    Rules:
    - Split cookie pairs on ';'
    - Split each pair on the FIRST '=' only
    - Trim whitespace around keys and values
    - Ignore segments with no '='
    - For duplicate keys, the last value wins
    """
    result = {}
    
    # Split on semicolons
    pairs = header.split(';')
    
    for pair in pairs:
        # Split on the first '=' only
        if '=' not in pair:
            # Ignore segments with no '='
            continue
        
        # Split on first '=' only
        key, value = pair.split('=', 1)
        
        # Trim whitespace
        key = key.strip()
        value = value.strip()
        
        # Add to result (last value wins for duplicates)
        result[key] = value
    
    return result
