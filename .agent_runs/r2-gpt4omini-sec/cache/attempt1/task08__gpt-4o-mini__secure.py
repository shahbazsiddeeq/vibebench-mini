# src/solution.py

import urllib.parse
import re
import secrets

def normalize_url(url: str) -> str:
    # Validate input
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Parse the URL
    parsed = urllib.parse.urlparse(url)

    # Default scheme to 'https' if missing
    scheme = parsed.scheme.lower() if parsed.scheme else 'https'
    
    # Lowercase the host, preserve userinfo
    userinfo = parsed.username + (':' + parsed.password if parsed.password else '') if parsed.username else ''
    host = parsed.hostname.lower() if parsed.hostname else ''
    
    # Handle default ports
    port = parsed.port
    if (scheme == 'http' and port == 80) or (scheme == 'https' and port == 443):
        port = None

    # Normalize the path
    path = normalize_path(parsed.path)

    # Sort query parameters
    query = normalize_query(parsed.query)

    # Construct the normalized URL
    normalized_url = urllib.parse.urlunparse((
        scheme,
        f"{userinfo}@{host}" if userinfo else host,
        path,
        '',  # No params
        query,
        ''   # No fragment
    ))

    return normalized_url

def normalize_path(path: str) -> str:
    # Resolve dot-segments and collapse consecutive slashes
    normalized_path = re.sub(r'/+', '/', path)  # Collapse slashes
    normalized_path = re.sub(r'/\./', '/', normalized_path)  # Remove './'
    normalized_path = re.sub(r'/[^/]+/\.\./', '/', normalized_path)  # Remove '../'
    normalized_path = re.sub(r'/[^/]+$', '', normalized_path)  # Remove trailing segments
    return normalized_path if normalized_path else '/'

def normalize_query(query: str) -> str:
    # Parse query parameters
    params = urllib.parse.parse_qs(query, keep_blank_values=True)
    # Sort parameters by key
    sorted_params = sorted(params.items())
    # Reconstruct the query string
    normalized_query = urllib.parse.urlencode(sorted_params, doseq=True)
    return normalized_query
