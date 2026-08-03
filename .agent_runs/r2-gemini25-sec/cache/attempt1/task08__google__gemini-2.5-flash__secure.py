import re
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def normalize_url(url: str) -> str:
    """
    Normalizes a URL to its canonical form.

    Applies the following rules:
    1. If the input has no scheme, default to "https".
    2. Lowercase the scheme and the host. Userinfo ("user:pass@") is preserved verbatim (case kept).
    3. Drop the default port for the scheme (80 for http, 443 for https); keep any other port.
    4. Normalize the path: resolve "." and ".." dot-segments and collapse runs of consecutive
       slashes into one. An empty path becomes "/". A trailing slash is preserved.
    5. Sort the query parameters by key (blank values are kept, e.g. "a=").
    6. Drop the fragment.

    Args:
        url: The URL string to normalize.

    Returns:
        The normalized URL string.
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string.")

    # Prepend 'https://' if no scheme is present
    if "://" not in url:
        url = "https://" + url

    try:
        parsed = urlparse(url)
    except Exception as e:
        # Catch potential parsing errors, though urlparse is quite robust
        raise ValueError(f"Invalid URL format: {url}") from e

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc
    path = parsed.path
    query = parsed.query
    # Fragment is dropped, so we don't need to process it

    # Rule 2: Lowercase scheme and host. Userinfo is preserved.
    # Split netloc into userinfo and host:port
    userinfo_match = re.match(r"^(.*@)(.*)$", netloc)
    if userinfo_match:
        userinfo = userinfo_match.group(1)
        host_port = userinfo_match.group(2)
    else:
        userinfo = ""
        host_port = netloc

    # Split host_port into host and port
    host_match = re.match(r"^(.*):(\d+)$", host_port)
    if host_match:
        host = host_match.group(1).lower()
        port = host_match.group(2)
    else:
        host = host_port.lower()
        port = ""

    # Rule 3: Drop default port
    if (scheme == "http" and port == "80") or \
       (scheme == "https" and port == "443"):
        port = ""

    # Reconstruct netloc
    if port:
        netloc = f"{userinfo}{host}:{port}"
    else:
        netloc = f"{userinfo}{host}"

    # Rule 4: Normalize path
    # Collapse runs of consecutive slashes
    path = re.sub(r"//+", "/", path)

    # Resolve "." and ".." dot-segments
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

    # Reconstruct path, preserving trailing slash if original had one
    if not normalized_segments:
        path = "/"
    else:
        path = "/" + "/".join(normalized_segments)
        if parsed.path.endswith('/') and path != '/':
            path += '/'

    # Rule 5: Sort query parameters by key
    if query:
        # parse_qs returns a dict where values are lists.
        # We need to handle cases like 'a=1&a=2' and 'a='
        parsed_query = parse_qs(query, keep_blank_values=True)
        sorted_query_items = []
        for key in sorted(parsed_query.keys()):
            # urlencode handles lists of values correctly, e.g., {'a': ['1', '2']} -> 'a=1&a=2'
            # For blank values, parse_qs gives [''] for 'a=', which urlencode handles.
            for value in parsed_query[key]:
                sorted_query_items.append((key, value))
        query = urlencode(sorted_query_items, doseq=True)
    else:
        query = ""

    # Rule 6: Drop the fragment (already handled by not including parsed.fragment)

    # Reconstruct the URL
    normalized_url = urlunparse((scheme, netloc, path, "", query, ""))
    return normalized_url
