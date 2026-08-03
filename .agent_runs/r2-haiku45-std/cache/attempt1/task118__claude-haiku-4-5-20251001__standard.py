def flatten_dict(d, sep="."):
    """
    Flattens a nested dictionary into a single-level dict with keys joined by sep.
    
    Args:
        d: A dictionary to flatten
        sep: Separator to use when joining keys (default ".")
    
    Returns:
        A flattened dictionary
    
    Raises:
        ValueError: If two different paths collapse to the same flattened key
    """
    result = {}
    
    def _flatten(obj, prefix=""):
        """
        Recursively flatten the dictionary.
        
        Args:
            obj: Current object being processed
            prefix: Current key prefix
        """
        if isinstance(obj, dict):
            # If dict is empty, treat it as a leaf
            if not obj:
                if prefix:
                    if prefix in result:
                        raise ValueError(f"Separator collision: key '{prefix}' already exists")
                    result[prefix] = {}
            else:
                # Recursively process each key-value pair
                for key, value in obj.items():
                    new_key = f"{prefix}{sep}{key}" if prefix else key
                    _flatten(value, new_key)
        else:
            # Non-dict value is a leaf
            if prefix in result:
                raise ValueError(f"Separator collision: key '{prefix}' already exists")
            result[prefix] = obj
    
    _flatten(d)
    return result
