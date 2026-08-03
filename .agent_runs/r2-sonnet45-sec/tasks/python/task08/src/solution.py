import re
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from posixpath import normpath


def normalize_url(url: str) -> str:
    """
    Normalize a URL to a canonical form.
    
    Rules:
    1. If no scheme, default to "https"
    2. Lowercase scheme and host (preserve userinfo case)
    3. Drop default ports (80 for http, 443 for https)
    4. Normalize path (resolve . and .., collapse slashes, empty -> /)
    5. Sort query parameters by key
    6. Drop fragment
    """
    # Input validation
    if not isinstance(url, str):
        raise TypeError("URL must be a string")
    
    url = url.strip()
    if not url:
        raise ValueError("URL cannot be empty")
    
    # Add scheme if missing
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', url):
        url = 'https://' + url
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Extract components
    scheme = parsed.scheme.lower() if parsed.scheme else 'https'
    netloc = parsed.netloc
    path = parsed.path
    query = parsed.query
    
    # Process netloc: separate userinfo from host
    userinfo = ''
    host_port = netloc
    
    if '@' in netloc:
        userinfo, host_port = netloc.rsplit('@', 1)
        userinfo += '@'
    
    # Separate host and port
    host = host_port
    port = ''
    
    # Handle IPv6 addresses
    if host_port.startswith('['):
        # IPv6 address
        if ']' in host_port:
            bracket_end = host_port.index(']')
            host = host_port[:bracket_end + 1]
            remainder = host_port[bracket_end + 1:]
            if remainder.startswith(':'):
                port = remainder[1:]
    else:
        # Regular host or IPv4
        if ':' in host_port:
            host, port = host_port.rsplit(':', 1)
    
    # Lowercase the host
    host = host.lower()
    
    # Remove default ports
    default_ports = {'http': '80', 'https': '443'}
    if port == default_ports.get(scheme, ''):
        port = ''
    
    # Reconstruct netloc
    netloc = userinfo + host
    if port:
        netloc += ':' + port
    
    # Normalize path
    if not path:
        path = '/'
    else:
        # Preserve trailing slash
        trailing_slash = path.endswith('/')
        
        # Collapse consecutive slashes and resolve . and ..
        # Split path into segments
        segments = path.split('/')
        normalized_segments = []
        
        for segment in segments:
            if segment == '' or segment == '.':
                continue
            elif segment == '..':
                if normalized_segments:
                    normalized_segments.pop()
            else:
                normalized_segments.append(segment)
        
        # Reconstruct path
        if normalized_segments:
            path = '/' + '/'.join(normalized_segments)
        else:
            path = '/'
        
        # Restore trailing slash if it was present and path is not just "/"
        if trailing_slash and path != '/':
            path += '/'
    
    # Sort query parameters
    if query:
        # Parse query string
        params = parse_qsl(query, keep_blank_values=True)
        # Sort by key
        params.sort(key=lambda x: x[0])
        # Reconstruct query string
        query = urlencode(params)
    
    # Reconstruct URL without fragment
    normalized = urlunparse((scheme, netloc, path, '', query, ''))
    
    return normalized
