# src/solution.py

import urllib.parse
from typing import Dict, List

def parse_query_string(qs: str) -> Dict[str, List[str]]:
    # Validate input
    if not isinstance(qs, str):
        raise ValueError("Input must be a string")
    
    # Initialize the result dictionary
    result = {}
    
    # Split the query string by '&'
    pairs = qs.split('&')
    
    for pair in pairs:
        # Skip empty segments
        if pair == '':
            continue
        
        # Split on the first '=' only
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key, value = pair, ''
        
        # Decode key and value
        decoded_key = urllib.parse.unquote_plus(key)
        decoded_value = urllib.parse.unquote_plus(value)
        
        # Append the value to the list for the key
        if decoded_key in result:
            result[decoded_key].append(decoded_value)
        else:
            result[decoded_key] = [decoded_value]
    
    return result
