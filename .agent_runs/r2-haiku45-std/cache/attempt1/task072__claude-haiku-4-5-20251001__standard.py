def parse_url(url):
    """
    Parse a URL and return a dictionary with its components.
    
    Args:
        url: A URL string to parse
        
    Returns:
        A dictionary with keys: scheme, host, port, path, query_params, fragment
        
    Raises:
        ValueError: If scheme or host is missing
    """
    # Remove leading/trailing whitespace
    url = url.strip()
    
    # Extract fragment
    if '#' in url:
        url, fragment = url.rsplit('#', 1)
    else:
        fragment = ""
    
    # Extract query string
    if '?' in url:
        url, query_string = url.rsplit('?', 1)
    else:
        query_string = ""
    
    # Parse scheme
    if '://' not in url:
        raise ValueError("Missing scheme")
    
    scheme, rest = url.split('://', 1)
    
    # Parse host and port
    # Need to handle path after host:port
    if '/' in rest:
        host_port, path = rest.split('/', 1)
        path = '/' + path
    else:
        host_port = rest
        path = "/"
    
    # Parse host and port
    if ':' in host_port:
        host, port_str = host_port.rsplit(':', 1)
        try:
            port = int(port_str)
        except ValueError:
            raise ValueError("Invalid port")
    else:
        host = host_port
        port = None
    
    # Validate host
    if not host:
        raise ValueError("Missing host")
    
    # Lowercase host
    host = host.lower()
    
    # Parse query parameters
    query_params = {}
    if query_string:
        for param in query_string.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                # Drop parameters with blank/missing values
                if value:
                    if key in query_params:
                        # Convert to list if multiple values
                        if isinstance(query_params[key], list):
                            query_params[key].append(value)
                        else:
                            query_params[key] = [query_params[key], value]
                    else:
                        query_params[key] = value
            else:
                # Parameter without '=' (e.g., "a") - drop it
                pass
    
    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment,
    }
