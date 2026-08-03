def deep_merge(base, override):
    """
    Recursively merges two dicts. Override values take precedence.
    Nested dicts are merged recursively. Non-dict values from override replace base values.
    Returns a new dict without modifying inputs.
    """
    # Start with a shallow copy of base
    result = base.copy()
    
    # Process each key in override
    for key, override_value in override.items():
        if key in result:
            base_value = result[key]
            # If both values are dicts, merge them recursively
            if isinstance(base_value, dict) and isinstance(override_value, dict):
                result[key] = deep_merge(base_value, override_value)
            else:
                # Otherwise, override value replaces base value
                result[key] = override_value
        else:
            # Key only in override, just add it
            result[key] = override_value
    
    return result
