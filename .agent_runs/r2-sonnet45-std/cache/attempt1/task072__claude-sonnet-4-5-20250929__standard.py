def parse_url(url):
    """
    Parse a URL into its components.
    
    Returns a dict with keys: scheme, host, port, path, query_params, fragment.
    Raises ValueError if scheme or host is missing.
    """
    # Find scheme
    if "://" not in url:
        raise ValueError("Missing scheme")
    
    scheme, rest = url.split("://", 1)
    if not scheme:
        raise ValueError("Missing scheme")
    
    # Extract fragment first
    fragment = ""
    if "#" in rest:
        rest, fragment = rest.split("#", 1)
    
    # Extract query string
    query_string = ""
    if "?" in rest:
        rest, query_string = rest.split("?", 1)
    
    # Now rest contains: [host][:port][/path]
    # Split by first "/" to separate host:port from path
    if "/" in rest:
        host_port, path = rest.split("/", 1)
        path = "/" + path
    else:
        host_port = rest
        path = "/"
    
    # Parse host and port
    if not host_port:
        raise ValueError("Missing host")
    
    port = None
    if ":" in host_port:
        # Check if this is IPv6 or host:port
        # For simplicity, assume last colon is port separator
        # (IPv6 would need brackets which we'll handle separately)
        host, port_str = host_port.rsplit(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            # Not a valid port, treat whole thing as host
            host = host_port
            port = None
    else:
        host = host_port
    
    if not host:
        raise ValueError("Missing host")
    
    host = host.lower()
    
    # Parse query parameters
    query_params = {}
    if query_string:
        pairs = query_string.split("&")
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                # Drop blank values
                if value == "":
                    continue
            else:
                # Parameter without value (e.g., "a")
                # According to spec, these are dropped
                continue
            
            # Handle multiple occurrences
            if key in query_params:
                # Convert to list if not already
                if isinstance(query_params[key], list):
                    query_params[key].append(value)
                else:
                    query_params[key] = [query_params[key], value]
            else:
                query_params[key] = value
    
    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment,
    }
