from urllib.parse import unquote_plus


def parse_query_string(qs: str) -> dict[str, list[str]]:
    """
    Parse a URL query string into a dict mapping keys to lists of values.
    
    - Pairs are separated by '&'
    - Within a pair, split on the FIRST '=' only
    - Segments with no '=' become that key with empty-string value
    - Empty segments (from leading/trailing/doubled '&') are skipped
    - Both keys and values are percent-decoded with '+' -> space
    - Repeated keys accumulate in order
    - Keys are case-sensitive
    - Empty string returns {}
    """
    if not qs:
        return {}
    
    result: dict[str, list[str]] = {}
    
    # Split by '&' to get individual pairs
    pairs = qs.split('&')
    
    for pair in pairs:
        # Skip empty segments
        if not pair:
            continue
        
        # Split on the FIRST '=' only
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key = pair
            value = ''
        
        # Decode key and value using unquote_plus (handles % decoding and + -> space)
        decoded_key = unquote_plus(key)
        decoded_value = unquote_plus(value)
        
        # Append to the list for this key
        if decoded_key not in result:
            result[decoded_key] = []
        result[decoded_key].append(decoded_value)
    
    return result
