from urllib.parse import urlsplit, parse_qsl


def parse_url(url):
    parts = urlsplit(url)

    scheme = parts.scheme
    host = parts.hostname

    if not scheme or not host:
        raise ValueError("URL must have a scheme and a host")

    host = host.lower()
    port = parts.port

    path = parts.path if parts.path else "/"

    query_params = {}
    for key, value in parse_qsl(parts.query, keep_blank_values=False):
        if key in query_params:
            if isinstance(query_params[key], list):
                query_params[key].append(value)
            else:
                query_params[key] = [query_params[key], value]
        else:
            query_params[key] = value

    fragment = parts.fragment if parts.fragment else ""

    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment,
    }
