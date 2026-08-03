from urllib.parse import unquote_plus


def parse_query_string(qs: str) -> dict[str, list[str]]:
    """
    Parse a URL query string into a dict mapping keys to lists of values.
    
    Args:
        qs: Query string without leading '?'
        
    Returns:
        Dict mapping decoded keys to ordered lists of decoded values
    """
    if not qs:
        return {}
    
    result = {}
    
    # Split by '&' to get key-value pairs
    segments = qs.split('&')
    
    for segment in segments:
        # Skip empty segments
        if not segment:
            continue
        
        # Split on first '=' only
        if '=' in segment:
            key, value = segment.split('=', 1)
        else:
            # No '=' means key with empty value
            key = segment
            value = ''
        
        # Decode key and value
        key = unquote_plus(key)
        value = unquote_plus(value)
        
        # Add to result, accumulating values for repeated keys
        if key not in result:
            result[key] = []
        result[key].append(value)
    
    return result
