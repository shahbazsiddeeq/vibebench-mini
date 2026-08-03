def flatten_dict(d, sep="."):
    """
    Flatten a nested dictionary into a single-level dict with keys joined by sep.
    
    Args:
        d: Dictionary to flatten
        sep: Separator to use for joining keys (default ".")
    
    Returns:
        Flattened dictionary
        
    Raises:
        ValueError: If two different paths collapse to the same flattened key
    """
    if not d:
        return {}
    
    result = {}
    
    def _flatten(obj, prefix=""):
        if not isinstance(obj, dict) or len(obj) == 0:
            # Leaf node (non-dict or empty dict)
            if prefix in result:
                raise ValueError(f"Key collision: {prefix}")
            result[prefix] = obj
        else:
            # Non-empty dict - recurse
            for key, value in obj.items():
                new_key = f"{prefix}{sep}{key}" if prefix else key
                _flatten(value, new_key)
    
    _flatten(d)
    return result
