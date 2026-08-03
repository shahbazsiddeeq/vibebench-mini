def parse_cookie(header: str) -> dict:
    """
    Parse a Cookie header string into a dictionary.
    
    Rules:
    - Split cookie pairs on ';'
    - Split each pair on the FIRST '=' only
    - Trim whitespace around keys and values
    - Ignore segments with no '='
    - For duplicate keys, the last value wins
    
    Args:
        header: Cookie header string of the form "key=value; key2=value2"
    
    Returns:
        Dictionary mapping cookie names to values
    """
    if not isinstance(header, str):
        return {}
    
    result = {}
    
    # Split on semicolon to get individual cookie pairs
    pairs = header.split(';')
    
    for pair in pairs:
        # Skip empty pairs
        if not pair:
            continue
        
        # Find the first '=' to split key and value
        equals_index = pair.find('=')
        
        # Ignore segments with no '='
        if equals_index == -1:
            continue
        
        # Split on the first '=' only
        key = pair[:equals_index].strip()
        value = pair[equals_index + 1:].strip()
        
        # Only add if key is not empty
        if key:
            result[key] = value
    
    return result
