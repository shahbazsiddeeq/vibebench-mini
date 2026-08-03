from urllib.parse import unquote_plus
from collections import defaultdict

def parse_query_string(qs: str) -> dict[str, list[str]]:
    result = defaultdict(list)
    
    if not qs:
        return {}
    
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
        
        result[decoded_key].append(decoded_value)
    
    return dict(result)
