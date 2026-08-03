from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import re
import secrets

def normalize_url(url: str) -> str:
    # Add scheme if missing
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', url):
        url = 'https://' + url

    # Parse the URL
    parsed_url = urlparse(url)

    # Lowercase scheme and host
    scheme = parsed_url.scheme.lower()
    host = parsed_url.hostname.lower() if parsed_url.hostname else ''

    # Handle default ports
    port = parsed_url.port
    if (scheme == 'http' and port == 80) or (scheme == 'https' and port == 443):
        port = None

    # Normalize path
    path = re.sub(r'/+', '/', parsed_url.path)  # Collapse consecutive slashes
    segments = []
    for segment in path.split('/'):
        if segment == '..':
            if segments:
                segments.pop()
        elif segment != '.' and segment != '':
            segments.append(segment)
    path = '/' + '/'.join(segments)
    if parsed_url.path.endswith('/') and not path.endswith('/'):
        path += '/'

    # Sort query parameters
    query = urlencode(sorted(parse_qsl(parsed_url.query, keep_blank_values=True)))

    # Reconstruct the URL without fragment
    normalized_url = urlunparse((
        scheme,
        f"{parsed_url.username or ''}{':' if parsed_url.username else ''}{parsed_url.password or ''}@{host}{':' + str(port) if port else ''}",
        path or '/',
        parsed_url.params,
        query,
        ''
    ))

    return normalized_url
