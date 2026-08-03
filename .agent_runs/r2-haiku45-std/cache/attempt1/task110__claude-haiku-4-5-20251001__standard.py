def deep_merge(base, override):
    """
    Recursively merges two dicts; override values take precedence.
    
    Nested dicts are merged recursively, not replaced. When a key exists in both
    and either side is not a dict (including lists), the override value replaces
    the base value outright (lists are not concatenated).
    
    Returns a new top-level dict without modifying either input; nested dict values
    taken unchanged from base are shared (not deep-copied) with base.
    
    Args:
        base: The base dictionary
        override: The override dictionary
        
    Returns:
        A new merged dictionary
    """
    result = {}
    
    # First, add all items from base
    for key, value in base.items():
        result[key] = value
    
    # Then, merge in items from override
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Both are dicts, so recursively merge them
            result[key] = deep_merge(result[key], value)
        else:
            # Either key doesn't exist in result, or one/both values aren't dicts
            # In either case, override takes precedence
            result[key] = value
    
    return result
