from urllib.parse import urlparse, parse_qs

def parse_url(url):
    parsed_url = urlparse(url)

    scheme = parsed_url.scheme
    host = parsed_url.hostname
    port = parsed_url.port
    path = parsed_url.path
    query = parsed_url.query
    fragment = parsed_url.fragment

    if not scheme:
        raise ValueError("Scheme is missing")
    if not host:
        raise ValueError("Host is missing")

    host = host.lower()

    if not path:
        path = "/"

    query_params = {}
    if query:
        parsed_qs = parse_qs(query, keep_blank_values=True)
        for key, values in parsed_qs.items():
            filtered_values = [v for v in values if v]  # Drop blank values
            if filtered_values:
                if len(filtered_values) == 1:
                    query_params[key] = filtered_values[0]
                else:
                    query_params[key] = filtered_values

    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment,
    }
