from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import re


def normalize_url(url: str) -> str:
    """
    Normalize a URL according to the specified rules.
    
    Rules:
    1. If no scheme, default to "https"
    2. Lowercase scheme and host; preserve userinfo case
    3. Drop default ports (80 for http, 443 for https)
    4. Normalize path: resolve dots, collapse slashes, empty path becomes "/"
    5. Sort query parameters by key
    6. Drop fragment
    """
    
    # Add default scheme if missing
    if "://" not in url:
        url = "https://" + url
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Extract and normalize scheme
    scheme = parsed.scheme.lower()
    
    # Handle netloc (userinfo + host + port)
    netloc = parsed.netloc
    userinfo = ""
    hostport = netloc
    
    if "@" in netloc:
        userinfo, hostport = netloc.rsplit("@", 1)
        userinfo += "@"
    
    # Split host and port
    if hostport.startswith("["):
        # IPv6 address
        if "]" in hostport:
            host, _, port_part = hostport.partition("]")
            host = host + "]"
            port_part = port_part.lstrip(":")
            port = port_part if port_part else ""
        else:
            host = hostport
            port = ""
    else:
        # IPv4 or hostname
        if ":" in hostport:
            host, port = hostport.rsplit(":", 1)
        else:
            host = hostport
            port = ""
    
    # Lowercase the host
    host = host.lower()
    
    # Remove default ports
    default_ports = {"http": "80", "https": "443"}
    if port == default_ports.get(scheme, ""):
        port = ""
    
    # Reconstruct netloc
    if port:
        netloc = userinfo + host + ":" + port
    else:
        netloc = userinfo + host
    
    # Normalize path
    path = parsed.path
    
    # Collapse consecutive slashes
    path = re.sub(r"/+", "/", path)
    
    # Resolve dot segments
    path = resolve_dot_segments(path)
    
    # Empty path becomes "/"
    if not path:
        path = "/"
    
    # Normalize query
    query = ""
    if parsed.query:
        # Parse query parameters
        params = parse_qsl(parsed.query, keep_blank_values=True)
        # Sort by key
        params.sort(key=lambda x: x[0])
        # Reconstruct query string
        query = urlencode(params)
    
    # Reconstruct URL without fragment
    normalized = urlunparse((scheme, netloc, path, "", query, ""))
    
    return normalized


def resolve_dot_segments(path: str) -> str:
    """
    Resolve . and .. dot-segments in a path.
    """
    # Split path into segments
    segments = path.split("/")
    output = []
    
    for segment in segments:
        if segment == "." or segment == "":
            # "." is current directory, empty is from consecutive slashes
            # Only add empty if it's the first segment (leading slash)
            if segment == "" and not output:
                output.append("")
            continue
        elif segment == "..":
            # Go up one directory if possible
            if output and output[-1] != "":
                output.pop()
            elif not output:
                # At root, can't go up
                pass
        else:
            output.append(segment)
    
    # Reconstruct path
    result = "/".join(output)
    
    # Ensure leading slash if original path had it
    if path.startswith("/") and not result.startswith("/"):
        result = "/" + result
    
    # Preserve trailing slash if original had it (and path is not just "/")
    if path.endswith("/") and path != "/" and not result.endswith("/"):
        result += "/"
    
    return result
