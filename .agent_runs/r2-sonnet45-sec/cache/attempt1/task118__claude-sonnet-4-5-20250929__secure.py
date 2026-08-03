def flatten_dict(d, sep="."):
    """
    Flatten a nested dictionary into a single-level dict with keys joined by sep.
    
    Args:
        d: Dictionary to flatten
        sep: Separator string to join keys (default ".")
    
    Returns:
        Flattened dictionary
        
    Raises:
        ValueError: If separator collision occurs or invalid inputs
        TypeError: If d is not a dict or sep is not a string
    """
    # Input validation
    if not isinstance(d, dict):
        raise TypeError("First argument must be a dictionary")
    
    if not isinstance(sep, str):
        raise TypeError("Separator must be a string")
    
    # Empty dict returns empty dict
    if not d:
        return {}
    
    result = {}
    
    def _flatten(obj, prefix):
        """
        Recursively flatten the dictionary.
        
        Args:
            obj: Current object to process
            prefix: Current key prefix (list of key parts)
        """
        if not isinstance(obj, dict):
            # Non-dict value is a leaf
            key = sep.join(prefix)
            if key in result:
                raise ValueError(f"Separator collision: key '{key}' appears multiple times")
            result[key] = obj
        elif len(obj) == 0:
            # Empty dict is a leaf
            key = sep.join(prefix)
            if key in result:
                raise ValueError(f"Separator collision: key '{key}' appears multiple times")
            result[key] = {}
        else:
            # Non-empty dict: recurse into it
            for k, v in obj.items():
                # Validate that keys are strings
                if not isinstance(k, str):
                    raise TypeError(f"Dictionary keys must be strings, got {type(k).__name__}")
                
                new_prefix = prefix + [k]
                _flatten(v, new_prefix)
    
    # Process top-level keys
    for key, value in d.items():
        # Validate that keys are strings
        if not isinstance(key, str):
            raise TypeError(f"Dictionary keys must be strings, got {type(key).__name__}")
        
        _flatten(value, [key])
    
    return result
