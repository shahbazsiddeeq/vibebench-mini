import urllib.parse

def normalize_url(url):
    if "://" not in url:
        url = "https://" + url

    parsed = urllib.parse.urlparse(url)

    scheme = parsed.scheme.lower()
    netloc_parts = parsed.netloc.split('@', 1)
    userinfo = ""
    host_port = netloc_parts[-1]

    if len(netloc_parts) > 1:
        userinfo = netloc_parts[0] + '@'

    host = host_port
    port = ""
    if ':' in host_port:
        host, port = host_port.rsplit(':', 1)

    host = host.lower()

    # Drop default port
    if (scheme == "http" and port == "80") or \
       (scheme == "https" and port == "443"):
        port = ""

    if port:
        netloc = userinfo + host + ":" + port
    else:
        netloc = userinfo + host

    # Normalize path
    path_segments = []
    for segment in parsed.path.split('/'):
        if segment == "" or segment == ".":
            continue
        if segment == "..":
            if path_segments:
                path_segments.pop()
        else:
            path_segments.append(segment)

    normalized_path = "/" + "/".join(path_segments)
    if not normalized_path:
        normalized_path = "/"
    # Preserve trailing slash if original path had one and it's not just "/"
    if parsed.path.endswith('/') and normalized_path != "/":
        normalized_path += "/"


    # Sort query parameters
    query_params = urllib.parse.parse_qsl(parsed.query)
    query_params.sort(key=lambda x: x[0])
    normalized_query = urllib.parse.urlencode(query_params)

    # Drop fragment
    fragment = ""

    return urllib.parse.urlunparse((scheme, netloc, normalized_path, parsed.params, normalized_query, fragment))
