# src/solution.py

from urllib.parse import urlparse, parse_qs

def parse_url(url):
    parsed = urlparse(url)
    
    if not parsed.scheme or not parsed.hostname:
        raise ValueError("URL must have a scheme and a host.")
    
    scheme = parsed.scheme
    host = parsed.hostname.lower()
    port = parsed.port
    path = parsed.path if parsed.path else "/"
    fragment = parsed.fragment
    
    raw_query_params = parse_qs(parsed.query)
    query_params = {}
    
    for key, values in raw_query_params.items():
        filtered_values = [v for v in values if v]
        if len(filtered_values) == 1:
            query_params[key] = filtered_values[0]
        elif len(filtered_values) > 1:
            query_params[key] = filtered_values
    
    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment
    }
