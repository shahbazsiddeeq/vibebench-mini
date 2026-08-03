# src/solution.py

from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import posixpath

def normalize_url(url):
    # Parse the URL
    parsed = urlparse(url, scheme='https')
    
    # Lowercase the scheme and host
    scheme = parsed.scheme.lower()
    host = parsed.hostname.lower() if parsed.hostname else ''
    
    # Preserve userinfo
    userinfo = f"{parsed.username}:{parsed.password}@" if parsed.username and parsed.password else ''
    
    # Handle port
    port = parsed.port
    if (scheme == 'http' and port == 80) or (scheme == 'https' and port == 443):
        port = None
    
    # Normalize the path
    path = posixpath.normpath(parsed.path)
    if not path or path == '.':
        path = '/'
    if parsed.path.endswith('/') and not path.endswith('/'):
        path += '/'
    
    # Sort query parameters
    query = urlencode(sorted(parse_qsl(parsed.query, keep_blank_values=True)))
    
    # Reconstruct the URL without the fragment
    normalized_url = urlunparse((
        scheme,
        f"{userinfo}{host}" + (f":{port}" if port else ''),
        path,
        parsed.params,
        query,
        ''
    ))
    
    return normalized_url
