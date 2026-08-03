"""
URL Normalizer

Provides `normalize_url(url)` which returns a canonical form of a URL
according to the following rules:

1. If the input has no scheme, default to "https".
2. Lowercase the scheme and the host. Userinfo ("user:pass@") is preserved
   verbatim (case kept).
3. Drop the default port for the scheme (80 for http, 443 for https); keep
   any other port.
4. Normalize the path: resolve "." and ".." dot-segments and collapse runs
   of consecutive slashes into one. An empty path becomes "/". A trailing
   slash is preserved.
5. Sort the query parameters by key (blank values are kept, e.g. "a=").
6. Drop the fragment.
"""

import re
from urllib.parse import urlsplit, parse_qsl, urlencode

_SCHEME_RE = re.compile(r'^[A-Za-z][A-Za-z0-9+.\-]*://')

_DEFAULT_PORTS = {
    'http': '80',
    'https': '443',
}


def _normalize_path(path):
    """Normalize a URL path: collapse slashes, resolve dot-segments."""
    if not path:
        return '/'

    # Collapse runs of consecutive slashes into a single slash.
    path = re.sub(r'/+', '/', path)

    trailing_slash = path.endswith('/') and path != '/'

    # Split into segments, dropping empty segments (caused by leading/
    # trailing slash) and "." segments.
    raw_parts = path.split('/')
    parts = [p for p in raw_parts if p != '' and p != '.']

    stack = []
    for part in parts:
        if part == '..':
            if stack:
                stack.pop()
            # if stack empty, ignore (don't go above root)
        else:
            stack.append(part)

    new_path = '/' + '/'.join(stack)

    if trailing_slash and new_path != '/':
        new_path += '/'

    if new_path == '':
        new_path = '/'

    return new_path


def normalize_url(url):
    """Return the canonical/normalized form of `url`."""
    if not _SCHEME_RE.match(url):
        url = 'https://' + url

    parts = urlsplit(url)

    scheme = parts.scheme.lower()
    netloc = parts.netloc

    # Separate userinfo from host:port
    if '@' in netloc:
        userinfo, hostport = netloc.rsplit('@', 1)
    else:
        userinfo = None
        hostport = netloc

    # Separate host and port (naive split, doesn't handle IPv6 brackets
    # specially, but sufficient for the required cases).
    if ':' in hostport:
        host, port = hostport.rsplit(':', 1)
    else:
        host = hostport
        port = None

    host = host.lower()

    default_port = _DEFAULT_PORTS.get(scheme)
    if port is not None and port == default_port:
        port = None

    new_netloc = ''
    if userinfo:
        new_netloc += userinfo + '@'
    new_netloc += host
    if port:
        new_netloc += ':' + port

    path = _normalize_path(parts.path)

    if parts.query:
        query_pairs = parse_qsl(parts.query, keep_blank_values=True)
        query_pairs.sort(key=lambda kv: kv[0])
        query = urlencode(query_pairs, doseq=False)
    else:
        query = ''

    result = f"{scheme}://{new_netloc}{path}"
    if query:
        result += '?' + query

    return result
