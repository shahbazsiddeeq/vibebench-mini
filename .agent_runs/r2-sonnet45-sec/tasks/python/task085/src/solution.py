from urllib.parse import urlencode


def build_query(params):
    """
    Build a URL query string from a dictionary.
    
    Args:
        params: Dictionary of query parameters. Values can be strings, integers,
                or lists. List values will result in repeated keys.
    
    Returns:
        URL-encoded query string with keys sorted alphabetically.
        Empty string if params is empty.
    
    Security considerations:
        - Uses urllib.parse.urlencode for proper URL encoding
        - Validates input types to prevent injection
        - Does not use eval/exec
    """
    if not params:
        return ""
    
    # Validate input is a dictionary
    if not isinstance(params, dict):
        raise TypeError("params must be a dictionary")
    
    # Build list of (key, value) tuples, expanding lists
    query_items = []
    
    # Sort keys alphabetically for consistent output
    for key in sorted(params.keys()):
        # Validate key is a string
        if not isinstance(key, (str, int)):
            raise TypeError(f"Key must be string or int, got {type(key)}")
        
        key_str = str(key)
        value = params[key]
        
        # Handle list values - repeat the key for each value
        if isinstance(value, list):
            for item in value:
                # Validate list items
                if not isinstance(item, (str, int, float, bool, type(None))):
                    raise TypeError(f"List item must be a simple type, got {type(item)}")
                query_items.append((key_str, str(item) if item is not None else ''))
        else:
            # Handle single values
            if not isinstance(value, (str, int, float, bool, type(None))):
                raise TypeError(f"Value must be a simple type, got {type(value)}")
            query_items.append((key_str, str(value) if value is not None else ''))
    
    # Use urlencode with doseq=True to handle the list of tuples
    # This properly URL-encodes values and uses '+' for spaces
    return urlencode(query_items)
