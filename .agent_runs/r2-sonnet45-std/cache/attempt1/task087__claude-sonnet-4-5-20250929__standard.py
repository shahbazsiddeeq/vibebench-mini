def parse_cookie(header):
    """
    Parse a Cookie header string into a dictionary.
    
    Args:
        header: Cookie header string of the form "key=value; key2=value2"
    
    Returns:
        dict: Parsed cookies with keys and values
    """
    result = {}
    
    # Split on semicolons to get individual cookie pairs
    pairs = header.split(';')
    
    for pair in pairs:
        # Check if there's an '=' in the pair
        if '=' not in pair:
            continue
        
        # Split on the first '=' only
        key, _, value = pair.partition('=')
        
        # Trim whitespace from key and value
        key = key.strip()
        value = value.strip()
        
        # Store in result (last value wins for duplicates)
        result[key] = value
    
    return result
