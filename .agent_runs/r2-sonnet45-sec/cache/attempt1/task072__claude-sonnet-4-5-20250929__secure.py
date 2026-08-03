def parse_url(url):
    """
    Parse a URL into its components.
    
    Args:
        url: A URL string to parse
        
    Returns:
        A dict with keys: scheme, host, port, path, query_params, fragment
        
    Raises:
        ValueError: If scheme or host is missing
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")
    
    # Initialize result
    result = {
        "scheme": None,
        "host": None,
        "port": None,
        "path": "/",
        "query_params": {},
        "fragment": ""
    }
    
    # Extract fragment first (everything after #)
    if "#" in url:
        url, fragment = url.split("#", 1)
        result["fragment"] = fragment
    
    # Extract scheme (everything before ://)
    if "://" not in url:
        raise ValueError("Missing scheme")
    
    scheme, rest = url.split("://", 1)
    if not scheme:
        raise ValueError("Missing scheme")
    result["scheme"] = scheme
    
    # Extract query string (everything after ?)
    query_string = ""
    if "?" in rest:
        rest, query_string = rest.split("?", 1)
    
    # Now rest contains: [host][:port][/path]
    # Extract path (everything after first /)
    if "/" in rest:
        host_port, path = rest.split("/", 1)
        result["path"] = "/" + path
    else:
        host_port = rest
        result["path"] = "/"
    
    # Extract host and port
    if not host_port:
        raise ValueError("Missing host")
    
    if ":" in host_port:
        # Check if this is IPv6 or host:port
        # For simplicity, assume it's host:port (IPv6 would be in brackets)
        parts = host_port.rsplit(":", 1)
        host = parts[0]
        port_str = parts[1]
        
        # Validate and convert port
        if port_str:
            try:
                port = int(port_str)
                if port < 0 or port > 65535:
                    raise ValueError("Invalid port number")
                result["port"] = port
            except ValueError:
                raise ValueError("Invalid port number")
        else:
            result["port"] = None
    else:
        host = host_port
    
    if not host:
        raise ValueError("Missing host")
    
    result["host"] = host.lower()
    
    # Parse query parameters
    if query_string:
        params = {}
        for param in query_string.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                # Drop parameters with blank/missing value
                if not value:
                    continue
            else:
                # Parameter without = is dropped
                continue
            
            # Handle duplicate keys
            if key in params:
                # Convert to list if not already
                if not isinstance(params[key], list):
                    params[key] = [params[key]]
                params[key].append(value)
            else:
                params[key] = value
        
        result["query_params"] = params
    
    return result
