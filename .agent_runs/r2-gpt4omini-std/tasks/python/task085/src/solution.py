# src/solution.py

import urllib.parse

def build_query(params):
    if not params:
        return ""
    
    query_parts = []
    
    for key in sorted(params.keys()):
        value = params[key]
        if isinstance(value, list):
            for item in value:
                query_parts.append(f"{urllib.parse.quote_plus(key)}={urllib.parse.quote_plus(str(item))}")
        else:
            query_parts.append(f"{urllib.parse.quote_plus(key)}={urllib.parse.quote_plus(str(value))}")
    
    return "&".join(query_parts)
