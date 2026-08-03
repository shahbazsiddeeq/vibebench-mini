from urllib.parse import urlencode

def build_query(params):
    """
    Build a URL query string from a dictionary.
    
    Args:
        params: Dictionary of parameters where values can be strings, numbers, or lists
        
    Returns:
        URL-encoded query string with keys sorted alphabetically
    """
    if not params:
        return ""
    
    # Convert params to a list of (key, value) tuples
    # Handle list values by creating multiple tuples with the same key
    items = []
    for key in sorted(params.keys()):
        value = params[key]
        if isinstance(value, list):
            for item in value:
                items.append((key, item))
        else:
            items.append((key, value))
    
    # Use urlencode which handles URL encoding and uses '+' for spaces
    return urlencode(items)
