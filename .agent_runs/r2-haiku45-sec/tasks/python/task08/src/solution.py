from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from pathlib import PurePosixPath


def normalize_url(url: str) -> str:
    """
    Normalize a URL to its canonical form.
    
    Rules:
    1. Default to "https" if no scheme
    2. Lowercase scheme and host; preserve userinfo case
    3. Drop default ports (80 for http, 443 for https)
    4. Normalize path: resolve dots, collapse slashes, ensure trailing slash for empty path
    5. Sort query parameters by key
    6. Drop fragment
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string")
    
    # Add default scheme if missing
    if "://" not in url:
        url = "https://" + url
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Extract and normalize scheme
    scheme = parsed.scheme.lower() if parsed.scheme else "https"
    
    # Extract userinfo and host
    netloc = parsed.netloc
    userinfo = ""
    host = netloc
    
    if "@" in netloc:
        userinfo, host = netloc.rsplit("@", 1)
        userinfo += "@"
    
    # Split host and port
    if host.startswith("["):
        # IPv6 address
        if "]" in host:
            ipv6_end = host.index("]")
            ipv6_part = host[:ipv6_end + 1]
            port_part = host[ipv6_end + 1:]
            host_only = ipv6_part
            port_str = port_part.lstrip(":")
        else:
            host_only = host
            port_str = ""
    else:
        # IPv4 or hostname
        if ":" in host:
            host_only, port_str = host.rsplit(":", 1)
        else:
            host_only = host
            port_str = ""
    
    # Lowercase the host
    host_only = host_only.lower()
    
    # Handle port: remove default ports
    port = None
    if port_str:
        try:
            port = int(port_str)
            default_port = 80 if scheme == "http" else 443 if scheme == "https" else None
            if port == default_port:
                port = None
        except ValueError:
            # Invalid port, keep as is
            port = port_str
    
    # Reconstruct netloc
    if port is not None:
        netloc = f"{userinfo}{host_only}:{port}"
    else:
        netloc = f"{userinfo}{host_only}"
    
    # Normalize path
    path = parsed.path
    if not path:
        path = "/"
    else:
        # Collapse consecutive slashes
        while "//" in path:
            path = path.replace("//", "/")
        
        # Resolve dot segments using PurePosixPath
        try:
            normalized_path = str(PurePosixPath(path))
            # PurePosixPath removes trailing slashes, so we need to preserve them
            if path.endswith("/") and not normalized_path.endswith("/"):
                normalized_path += "/"
            path = normalized_path
        except (ValueError, TypeError):
            # If path normalization fails, use the collapsed version
            pass
        
        # Ensure at least "/"
        if not path:
            path = "/"
    
    # Normalize query: sort parameters by key
    query = ""
    if parsed.query:
        # Parse query parameters, preserving blank values
        params = parse_qsl(parsed.query, keep_blank_values=True)
        # Sort by key
        params.sort(key=lambda x: x[0])
        # Reconstruct query string
        query = urlencode(params)
    
    # Reconstruct URL without fragment
    normalized = urlunparse((scheme, netloc, path, "", query, ""))
    
    return normalized
