from urllib.parse import quote_plus


def build_query(params):
    """
    Build a URL query string from a dictionary.
    
    - List values become repeated keys
    - Keys are sorted alphabetically
    - Values are URL-encoded (spaces as '+')
    - Empty dict returns empty string
    """
    if not params:
        return ""
    
    pairs = []
    
    # Sort keys alphabetically
    for key in sorted(params.keys()):
        value = params[key]
        
        # Handle list values
        if isinstance(value, list):
            for item in value:
                encoded_value = quote_plus(str(item))
                pairs.append(f"{key}={encoded_value}")
        else:
            # Convert to string and encode
            encoded_value = quote_plus(str(value))
            pairs.append(f"{key}={encoded_value}")
    
    return "&".join(pairs)
