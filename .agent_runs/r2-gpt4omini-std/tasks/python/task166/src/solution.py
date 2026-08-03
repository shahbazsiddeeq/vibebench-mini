# src/solution.py

from urllib.parse import unquote_plus

def parse_query_string(qs: str) -> dict[str, list[str]]:
    result = {}
    
    # Split the query string by '&'
    pairs = qs.split('&')
    
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)  # Split on the first '='
        else:
            key, value = pair, ''  # No '=' means empty value
        
        # Decode key and value
        decoded_key = unquote_plus(key)
        decoded_value = unquote_plus(value)
        
        # Skip empty segments
        if decoded_key or decoded_value:  # Only add if key or value is not empty
            if decoded_key not in result:
                result[decoded_key] = []
            result[decoded_key].append(decoded_value)
    
    return result
