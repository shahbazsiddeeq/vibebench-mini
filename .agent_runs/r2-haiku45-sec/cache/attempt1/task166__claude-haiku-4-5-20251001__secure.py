"""
Secure URL query string parser.
Parses query strings into a dict mapping keys to lists of values.
"""

from urllib.parse import unquote_plus
from typing import Dict, List


def parse_query_string(qs: str) -> Dict[str, List[str]]:
    """
    Parse a URL query string into a dict mapping decoded keys to lists of decoded values.
    
    Args:
        qs: Query string without leading '?'
        
    Returns:
        Dictionary mapping each key to an ordered list of its values.
        Both keys and values are percent-decoded with '+' decoded to space.
    """
    # Validate input type
    if not isinstance(qs, str):
        raise TypeError("Query string must be a string")
    
    # Handle empty string
    if not qs:
        return {}
    
    result: Dict[str, List[str]] = {}
    
    # Split by '&' to get individual segments
    segments = qs.split('&')
    
    for segment in segments:
        # Skip empty segments (from leading/trailing/doubled '&')
        if not segment:
            continue
        
        # Split on first '=' only
        if '=' in segment:
            key, value = segment.split('=', 1)
        else:
            # No '=' means key with empty string value
            key = segment
            value = ''
        
        # Decode key and value using unquote_plus (handles % escapes and + to space)
        decoded_key = unquote_plus(key)
        decoded_value = unquote_plus(value)
        
        # Append value to the list for this key
        if decoded_key not in result:
            result[decoded_key] = []
        result[decoded_key].append(decoded_value)
    
    return result
