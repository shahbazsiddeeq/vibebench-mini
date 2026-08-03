from urllib.parse import parse_qsl, urlsplit


def parse_url(url):
    """Parse a URL into its scheme, host, port, path, query, and fragment."""
    if not isinstance(url, str):
        raise ValueError("URL must be a string")
    if not url:
        raise ValueError("URL must include a scheme and host")
    if any(ord(char) < 32 or ord(char) == 127 for char in url):
        raise ValueError("URL contains invalid control characters")

    try:
        parsed = urlsplit(url)
        host = parsed.hostname
        port = parsed.port
    except (ValueError, UnicodeError):
        raise ValueError("Invalid URL") from None

    if not parsed.scheme or not host:
        raise ValueError("URL must include a scheme and host")

    query_params = {}
    try:
        pairs = parse_qsl(
            parsed.query,
            keep_blank_values=True,
            strict_parsing=False,
        )
    except (ValueError, UnicodeError):
        raise ValueError("Invalid URL query") from None

    for key, value in pairs:
        if value == "":
            continue

        if key not in query_params:
            query_params[key] = value
        else:
            existing = query_params[key]
            if isinstance(existing, list):
                existing.append(value)
            else:
                query_params[key] = [existing, value]

    return {
        "scheme": parsed.scheme,
        "host": host.lower(),
        "port": port,
        "path": parsed.path or "/",
        "query_params": query_params,
        "fragment": parsed.fragment,
    }
