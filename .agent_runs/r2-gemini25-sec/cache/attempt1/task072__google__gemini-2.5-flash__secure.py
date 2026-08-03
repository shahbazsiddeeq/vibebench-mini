import collections

def parse_url(url: str) -> dict:
    """
    Parses a URL string into its components.

    Args:
        url: The URL string to parse.

    Returns:
        A dictionary containing the parsed URL components:
        - scheme (str)
        - host (str, lowercased)
        - port (int or None)
        - path (str, defaults to "/" if no path component)
        - query_params (dict, keys map to single string or list of strings)
        - fragment (str, "" if absent)

    Raises:
        ValueError: If the scheme or host is missing.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string.")

    parsed_components = {
        "scheme": "",
        "host": "",
        "port": None,
        "path": "/",
        "query_params": {},
        "fragment": "",
    }

    # 1. Split fragment
    parts = url.split("#", 1)
    url_without_fragment = parts[0]
    if len(parts) > 1:
        parsed_components["fragment"] = parts[1]

    # 2. Split scheme
    scheme_parts = url_without_fragment.split("://", 1)
    if len(scheme_parts) == 1:
        raise ValueError("Scheme is missing.")
    
    parsed_components["scheme"] = scheme_parts[0]
    remaining = scheme_parts[1]

    # 3. Split host, port, path, query
    # Find the first '/' or '?' to separate authority from path/query
    path_query_start_index = -1
    for i, char in enumerate(remaining):
        if char == '/' or char == '?':
            path_query_start_index = i
            break

    authority = remaining
    if path_query_start_index != -1:
        authority = remaining[:path_query_start_index]
        remaining = remaining[path_query_start_index:]
    else:
        remaining = "" # No path or query

    # Parse authority (host and optional port)
    if not authority:
        raise ValueError("Host is missing.")

    host_port_parts = authority.split(":", 1)
    parsed_components["host"] = host_port_parts[0].lower()

    if not parsed_components["host"]:
        raise ValueError("Host is missing.")

    if len(host_port_parts) > 1:
        port_str = host_port_parts[1]
        if port_str:
            try:
                port = int(port_str)
                if not (0 <= port <= 65535):
                    raise ValueError("Port number out of range (0-65535).")
                parsed_components["port"] = port
            except ValueError:
                raise ValueError("Invalid port number.")

    # Parse path and query
    if remaining:
        path_query_parts = remaining.split("?", 1)
        path_component = path_query_parts[0]
        if path_component:
            parsed_components["path"] = path_component
        else:
            # If remaining starts with '?' (e.g., "example.com?k=v"), path is "/"
            parsed_components["path"] = "/"

        if len(path_query_parts) > 1:
            query_string = path_query_parts[1]
            parsed_components["query_params"] = _parse_query_string(query_string)
    
    # Ensure path is "/" if it's empty after parsing
    if not parsed_components["path"]:
        parsed_components["path"] = "/"

    return parsed_components

def _parse_query_string(query_string: str) -> dict:
    """
    Parses a URL query string into a dictionary.
    Handles multiple values for the same key and drops parameters with blank/missing values.
    """
    if not isinstance(query_string, str):
        raise ValueError("Query string must be a string.")

    params = collections.defaultdict(list)
    if not query_string:
        return {}

    for pair in query_string.split("&"):
        if not pair:
            continue
        
        key_value = pair.split("=", 1)
        key = key_value[0]
        value = key_value[1] if len(key_value) > 1 else ""

        # Drop parameters with blank/missing values
        if value:
            params[key].append(value)

    result = {}
    for key, values in params.items():
        if len(values) == 1:
            result[key] = values[0]
        elif len(values) > 1:
            result[key] = values
    return result
