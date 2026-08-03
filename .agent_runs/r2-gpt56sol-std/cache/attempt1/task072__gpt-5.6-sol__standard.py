from urllib.parse import parse_qsl, urlsplit


def parse_url(url):
    """Parse a URL into its scheme, host, port, path, query, and fragment."""
    parts = urlsplit(url)

    if not parts.scheme:
        raise ValueError("URL scheme is missing")
    if not parts.hostname:
        raise ValueError("URL host is missing")

    query_params = {}
    for key, value in parse_qsl(parts.query, keep_blank_values=False):
        if key in query_params:
            current = query_params[key]
            if isinstance(current, list):
                current.append(value)
            else:
                query_params[key] = [current, value]
        else:
            query_params[key] = value

    return {
        "scheme": parts.scheme,
        "host": parts.hostname.lower(),
        "port": parts.port,
        "path": parts.path or "/",
        "query_params": query_params,
        "fragment": parts.fragment,
    }
