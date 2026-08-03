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

    # Default scheme to 'https' if not present
    scheme = parsed.scheme.lower() if parsed.scheme else 'https'
    
    # Preserve userinfo case and lowercase host
    userinfo = parsed.username and parsed.password and f"{parsed.username}:{parsed.password}" or ""
    host = parsed.hostname.lower() if parsed.hostname else ""
    
    # Handle port
    port = parsed.port
    if (scheme == 'http' and port == 80) or (scheme == 'https' and port == 443):
        port = None

    # Normalize path
    path = urllib.parse.unquote(parsed.path)
    path = re.sub(r'/+', '/', path)  # Collapse consecutive slashes
    path = re.sub(r'/\.(?=/)', '', path)  # Remove single dot segments
    path = re.sub(r'/[^/]+/\.\./', '/', path)  # Remove double dot segments
    if path == '' or path == '.':
        path = '/'
    elif path.endswith('/'):
        path = path.rstrip('/') + '/'

    # Sort query parameters
    query_params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    sorted_query = sorted(query_params.items())
    normalized_query = urllib.parse.urlencode(sorted_query, doseq=True)

    # Construct the normalized URL
    normalized_url = urllib.parse.urlunparse((
        scheme,
        f"{userinfo}@{host}" if userinfo else host,
        path,
        '',  # No fragment
        normalized_query,
        ''   # No fragment
    ))

    return normalized_url
