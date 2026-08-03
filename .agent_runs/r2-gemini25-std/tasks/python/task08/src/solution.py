import urllib.parse

def normalize_url(url):
    # 1. If the input has no scheme, default to "https".
    if "://" not in url:
        url = "https://" + url

    parsed_url = urllib.parse.urlparse(url)

    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc
    path = parsed_url.path
    query = parsed_url.query
    
    # Split netloc into userinfo, host, and port
    userinfo = ""
    host = ""
    port = ""

    if "@" in netloc:
        userinfo, netloc = netloc.split("@", 1)
        userinfo += "@" # Preserve the @ for reconstruction
    
    if ":" in netloc:
        host, port = netloc.rsplit(":", 1)
    else:
        host = netloc

    # 2. Lowercase the scheme and the host. Userinfo ("user:pass@") is preserved verbatim (case kept).
    host = host.lower()

    # 3. Drop the default port for the scheme (80 for http, 443 for https); keep any other port.
    if (scheme == "http" and port == "80") or \
       (scheme == "https" and port == "443"):
        port = ""
    
    # Reconstruct netloc
    if port:
        netloc = f"{userinfo}{host}:{port}"
    else:
        netloc = f"{userinfo}{host}"

    # 4. Normalize the path: resolve "." and ".." dot-segments and collapse runs of consecutive
    #    slashes into one. An empty path becomes "/". A trailing slash is preserved.
    
    # Collapse runs of consecutive slashes
    path_parts = []
    for part in path.split('/'):
        if part: # Only add non-empty parts
            path_parts.append(part)
    
    # Resolve "." and ".." dot-segments
    resolved_path_parts = []
    for part in path_parts:
        if part == "." :
            pass
        elif part == "..":
            if resolved_path_parts:
                resolved_path_parts.pop()
        else:
            resolved_path_parts.append(part)
    
    # Handle empty path and trailing slash
    if not resolved_path_parts:
        path = "/"
    else:
        path = "/" + "/".join(resolved_path_parts)
        if parsed_url.path.endswith('/') and path != "/": # Preserve trailing slash if it was originally present and path is not just "/"
            path += "/"

    # 5. Sort the query parameters by key (blank values are kept, e.g. "a=").
    query_params = urllib.parse.parse_qsl(query, keep_blank_values=True)
    query_params.sort(key=lambda x: x[0])
    query = urllib.parse.urlencode(query_params, doseq=True)

    # 6. Drop the fragment.
    fragment = ""

    # Reconstruct the URL
    normalized_url = urllib.parse.urlunparse(
        urllib.parse.ParseResult(
            scheme=scheme,
            netloc=netloc,
            path=path,
            params="", # params are not handled in this task, typically empty for HTTP URLs
            query=query,
            fragment=fragment
        )
    )
    
    return normalized_url
