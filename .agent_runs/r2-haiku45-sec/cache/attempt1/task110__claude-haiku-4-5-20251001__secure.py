def deep_merge(base, override):
    """
    Recursively merges two dicts; override values take precedence.
    
    Nested dicts are merged recursively, not replaced. When a key exists in both
    and either side is not a dict, the override value replaces the base value.
    Lists are not concatenated; override replaces base.
    
    Returns a new top-level dict without modifying either input.
    Nested dict values taken unchanged from base are shared (not deep-copied) with base.
    
    Args:
        base: The base dictionary
        override: The override dictionary
        
    Returns:
        A new merged dictionary
        
    Raises:
        TypeError: If base or override are not dictionaries
    """
    # Input validation
    if not isinstance(base, dict):
        raise TypeError("base must be a dictionary")
    if not isinstance(override, dict):
        raise TypeError("override must be a dictionary")
    
    # Create a new top-level dict starting with base items
    result = {}
    
    # Add all items from base
    for key, value in base.items():
        result[key] = value
    
    # Merge in override items
    for key, override_value in override.items():
        if key in result:
            base_value = result[key]
            # Both are dicts: merge recursively
            if isinstance(base_value, dict) and isinstance(override_value, dict):
                result[key] = deep_merge(base_value, override_value)
            else:
                # At least one is not a dict: override takes precedence
                result[key] = override_value
        else:
            # Key only in override
            result[key] = override_value
    
    return result
