# src/solution.py

from urllib.parse import urlparse, parse_qs
from typing import Dict, Union

def parse_url(url: str) -> Dict[str, Union[str, int, None, Dict[str, Union[str, list]]]]:
    parsed = urlparse(url)
    
    if not parsed.scheme or not parsed.hostname:
        raise ValueError("URL must have a scheme and a host.")
    
    scheme = parsed.scheme
    host = parsed.hostname.lower()
    port = parsed.port
    path = parsed.path if parsed.path else "/"
    fragment = parsed.fragment if parsed.fragment else ""
    
    raw_query_params = parse_qs(parsed.query)
    query_params = {}
    
    for key, values in raw_query_params.items():
        # Filter out keys with empty values
        non_empty_values = [v for v in values if v]
        if non_empty_values:
            if len(non_empty_values) == 1:
                query_params[key] = non_empty_values[0]
            else:
                query_params[key] = non_empty_values
    
    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment
    }
