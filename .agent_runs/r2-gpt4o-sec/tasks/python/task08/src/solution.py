from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import secrets

def normalize_url(url: str) -> str:
    # Parse the URL
    parsed_url = urlparse(url, scheme='https')

    # Lowercase the scheme and host
    scheme = parsed_url.scheme.lower()
    host = parsed_url.hostname.lower() if parsed_url.hostname else ''

    # Preserve userinfo
    userinfo = ''
    if parsed_url.username:
        userinfo = parsed_url.username
        if parsed_url.password:
            userinfo += f':{parsed_url.password}'
        userinfo += '@'

    # Handle port
    port = parsed_url.port
    if (scheme == 'http' and port == 80) or (scheme == 'https' and port == 443):
        port = None

    # Normalize path
    path = parsed_url.path
    if not path:
        path = '/'
    else:
        segments = []
        for segment in path.split('/'):
            if segment == '..':
                if segments:
                    segments.pop()
            elif segment and segment != '.':
                segments.append(segment)
        path = '/' + '/'.join(segments)
        if path[-1] != '/' and parsed_url.path.endswith('/'):
            path += '/'

    # Sort query parameters
    query = urlencode(sorted(parse_qsl(parsed_url.query, keep_blank_values=True)))

    # Reconstruct the URL without fragment
    normalized_url = urlunparse((scheme, f'{userinfo}{host}' + (f':{port}' if port else ''), path, '', query, ''))

    return normalized_url
