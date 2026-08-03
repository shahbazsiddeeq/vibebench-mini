from urllib.parse import unquote_plus


def parse_query_string(qs: str) -> dict[str, list[str]]:
    """
    Parse a URL query string into a dict mapping keys to lists of values.
    
    Args:
        qs: Query string without leading '?' (e.g., 'a=1&b=2')
    
    Returns:
        Dict mapping each decoded key to an ordered list of its decoded values.
        
    Rules:
    - Pairs separated by '&'
    - Key/value split on FIRST '=' only
    - No '=' means key with empty string value
    - Empty segments (from &&, leading/trailing &) are skipped
    - Both keys and values are percent-decoded
    - '+' decoded to space (application/x-www-form-urlencoded)
    - Repeated keys accumulate values in order
    - Keys are case-sensitive
    """
    if not qs:
        return {}
    
    result: dict[str, list[str]] = {}
    
    # Split on '&' to get segments
    segments = qs.split('&')
    
    for segment in segments:
        # Skip empty segments
        if not segment:
            continue
        
        # Split on first '=' only
        if '=' in segment:
            key, _, value = segment.partition('=')
        else:
            # No '=' means key with empty value
            key = segment
            value = ''
        
        # Decode key and value (handles percent-encoding and + to space)
        decoded_key = unquote_plus(key)
        decoded_value = unquote_plus(value)
        
        # Append to list for this key (create list if first occurrence)
        if decoded_key not in result:
            result[decoded_key] = []
        result[decoded_key].append(decoded_value)
    
    return result
