from urllib.parse import urlparse, urlunparse, parse_qs, urlencode, quote, unquote
import re


def normalize_url(url):
    # Add scheme if missing
    if '://' not in url:
        url = 'https://' + url
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Extract components
    scheme = parsed.scheme.lower() if parsed.scheme else 'https'
    netloc = parsed.netloc
    path = parsed.path
    params = parsed.params
    query = parsed.query
    # fragment is dropped
    
    # Process netloc: lowercase host but preserve userinfo case
    if '@' in netloc:
        userinfo, host_port = netloc.rsplit('@', 1)
    else:
        userinfo = None
        host_port = netloc
    
    # Split host and port
    if ':' in host_port:
        # Handle IPv6 addresses
        if host_port.startswith('['):
            # IPv6
            if ']:' in host_port:
                host, port = host_port.rsplit(':', 1)
            else:
                host = host_port
                port = None
        else:
            # Regular host
            host, port = host_port.rsplit(':', 1)
    else:
        host = host_port
        port = None
    
    # Lowercase the host
    host = host.lower()
    
    # Remove default ports
    default_ports = {'http': '80', 'https': '443'}
    if port and port == default_ports.get(scheme):
        port = None
    
    # Reconstruct netloc
    if userinfo:
        netloc = userinfo + '@' + host
    else:
        netloc = host
    
    if port:
        netloc += ':' + port
    
    # Normalize path
    path = normalize_path(path)
    
    # Sort query parameters
    if query:
        query = sort_query(query)
    
    # Reconstruct URL (without fragment)
    normalized = urlunparse((scheme, netloc, path, params, query, ''))
    
    return normalized


def normalize_path(path):
    if not path:
        return '/'
    
    # Remember if path had trailing slash
    trailing_slash = path.endswith('/')
    
    # Split path into segments
    segments = path.split('/')
    
    # Process segments to resolve . and ..
    normalized_segments = []
    for segment in segments:
        if segment == '.' or segment == '':
            # Skip empty segments (from consecutive slashes) and current dir
            continue
        elif segment == '..':
            # Go up one level if possible
            if normalized_segments and normalized_segments[-1] != '..':
                normalized_segments.pop()
        else:
            normalized_segments.append(segment)
    
    # Reconstruct path
    if not normalized_segments:
        result = '/'
    else:
        result = '/' + '/'.join(normalized_segments)
    
    # Preserve trailing slash
    if trailing_slash and not result.endswith('/'):
        result += '/'
    
    return result


def sort_query(query):
    # Parse query string manually to preserve blank values
    params = []
    for part in query.split('&'):
        if '=' in part:
            key, value = part.split('=', 1)
            params.append((key, value))
        else:
            params.append((part, ''))
    
    # Sort by key
    params.sort(key=lambda x: x[0])
    
    # Reconstruct query string
    result = '&'.join(f'{k}={v}' if v or '=' in query.split('&')[0] else k 
                      for k, v in params)
    
    # Better reconstruction
    parts = []
    for k, v in params:
        if v or any('=' in p and p.split('=', 1)[0] == k for p in query.split('&')):
            parts.append(f'{k}={v}')
        else:
            parts.append(k)
    
    return '&'.join(parts)
