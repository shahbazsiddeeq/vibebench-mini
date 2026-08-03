def deep_merge(base, override):
    """
    Recursively merges two dicts; override values take precedence.
    
    Args:
        base: The base dictionary
        override: The override dictionary whose values take precedence
        
    Returns:
        A new dictionary with merged values. Nested dicts are merged recursively.
        When a key exists in both and either side is not a dict, the override 
        value replaces the base value. Lists are not concatenated.
        
    Security notes:
        - Validates inputs are dictionaries
        - Does not use eval/exec
        - Does not modify input dictionaries
        - Handles nested structures safely
    """
    # Validate inputs
    if not isinstance(base, dict):
        raise TypeError("base must be a dictionary")
    if not isinstance(override, dict):
        raise TypeError("override must be a dictionary")
    
    # Create a new dictionary to avoid mutating inputs
    result = {}
    
    # First, copy all items from base
    for key, value in base.items():
        result[key] = value
    
    # Then, merge/override with items from override
    for key, value in override.items():
        if key in result:
            # Key exists in both dictionaries
            base_value = result[key]
            
            # Only merge recursively if both values are dicts
            if isinstance(base_value, dict) and isinstance(value, dict):
                # Recursively merge the nested dicts
                result[key] = deep_merge(base_value, value)
            else:
                # Otherwise, override value replaces base value
                result[key] = value
        else:
            # Key only exists in override
            result[key] = value
    
    return result
