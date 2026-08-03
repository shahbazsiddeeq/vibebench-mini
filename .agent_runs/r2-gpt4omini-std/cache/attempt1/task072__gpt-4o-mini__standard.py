# src/solution.py

def parse_url(url):
    from urllib.parse import urlparse, parse_qs

    # Parse the URL
    parsed = urlparse(url)

    # Validate scheme and host
    if not parsed.scheme or not parsed.hostname:
        raise ValueError("Missing scheme or host")

    # Extract components
    scheme = parsed.scheme
    host = parsed.hostname.lower()
    port = parsed.port
    path = parsed.path if parsed.path else "/"
    fragment = parsed.fragment

    # Parse query parameters
    query_params = parse_qs(parsed.query, keep_blank_values=False)
    for key in query_params:
        if len(query_params[key]) == 1:
            query_params[key] = query_params[key][0]
        else:
            query_params[key] = [value for value in query_params[key] if value]

    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment,
    }
