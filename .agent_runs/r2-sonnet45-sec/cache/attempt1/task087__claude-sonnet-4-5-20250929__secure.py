def parse_cookie(header):
    """
    Parse a Cookie header string into a dictionary.
    
    Args:
        header: Cookie header string of the form "key=value; key2=value2"
    
    Returns:
        dict: Parsed cookies with keys and values as strings
    """
    if not isinstance(header, str):
        return {}
    
    result = {}
    
    # Split on semicolons to get individual cookie pairs
    pairs = header.split(';')
    
    for pair in pairs:
        # Strip whitespace from the pair
        pair = pair.strip()
        
        # Skip empty segments
        if not pair:
            continue
        
        # Check if there's an '=' in the pair
        if '=' not in pair:
            continue
        
        # Split on the first '=' only
        first_equals = pair.index('=')
        key = pair[:first_equals].strip()
        value = pair[first_equals + 1:].strip()
        
        # Only add if key is non-empty (security: avoid empty keys)
        if key:
            result[key] = value
    
    return result
