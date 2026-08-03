# src/solution.py

from urllib.parse import unquote_plus

def parse_query_string(qs: str) -> dict[str, list[str]]:
    result = {}
    
    if not qs:
        return result
    
    pairs = qs.split('&')
    
    for pair in pairs:
        if not pair:
            continue
        
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key, value = pair, ''
        
        decoded_key = unquote_plus(key)
        decoded_value = unquote_plus(value)
        
        if decoded_key in result:
            result[decoded_key].append(decoded_value)
        else:
            result[decoded_key] = [decoded_value]
    
    return result
