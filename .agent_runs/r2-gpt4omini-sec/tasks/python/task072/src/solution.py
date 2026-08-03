# src/solution.py

import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, List, Optional

def parse_url(url: str) -> Dict[str, Any]:
    # Validate input
    if not isinstance(url, str):
        raise ValueError("URL must be a string.")
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Extract components
    scheme = parsed.scheme
    host = parsed.hostname
    port = parsed.port
    path = parsed.path if parsed.path else "/"
    fragment = parsed.fragment if parsed.fragment else ""
    
    # Validate scheme and host
    if not scheme or not host:
        raise ValueError("Both scheme and host must be present.")
    
    # Lowercase the host
    host = host.lower()
    
    # Parse query parameters
    query_params = parse_qs(parsed.query, keep_blank_values=False)
    
    # Convert query parameters to the required format
    for key in query_params:
        if len(query_params[key]) == 1:
            query_params[key] = query_params[key][0]
        else:
            query_params[key] = [value for value in query_params[key] if value]
    
    # Remove empty values from query_params
    query_params = {k: v for k, v in query_params.items() if v}
    
    # Construct the result dictionary
    result = {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment,
    }
    
    return result
