# src/solution.py

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def normalize_url(url):
    # Parse the URL
    parsed = urlparse(url)
    
    # Default scheme to 'https' if not present
    scheme = parsed.scheme.lower() if parsed.scheme else 'https'
    
    # Lowercase the host, preserve userinfo
    userinfo = parsed.username + (':' + parsed.password if parsed.password else '') if parsed.username else ''
    host = parsed.hostname.lower() if parsed.hostname else ''
    
    # Drop default ports
    port = parsed.port
    if (scheme == 'http' and port == 80) or (scheme == 'https' and port == 443):
        port = None
    
    # Normalize the path
    path = parsed.path
    if path == '' or path == '/':
        normalized_path = '/'
    else:
        normalized_path = '/'.join(part for part in path.split('/') if part)  # Remove empty parts
        if parsed.path.endswith('/'):
            normalized_path += '/'
    
    # Sort query parameters
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    sorted_query = urlencode(sorted(query_params.items()), doseq=True)
    
    # Construct the normalized URL
    normalized_url = urlunparse((scheme, f"{userinfo}@{host}" if userinfo else host, normalized_path, '', sorted_query, ''))
    
    return normalized_url
