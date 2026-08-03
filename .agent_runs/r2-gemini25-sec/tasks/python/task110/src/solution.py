def deep_merge(base, override):
    """
    Recursively merges two dicts. Override values take precedence.
    Nested dicts are merged recursively, not replaced.
    When a key exists in both and either side is not a dict (including lists),
    the override value replaces the base value outright (lists are not concatenated).
    Returns a new top-level dict without modifying either input.
    Nested dict values taken unchanged from base are shared (not deep-copied) with base.

    Args:
        base (dict): The base dictionary.
        override (dict): The dictionary with overriding values.

    Returns:
        dict: A new dictionary representing the merged result.

    Raises:
        TypeError: If base or override are not dictionaries.
    """
    if not isinstance(base, dict):
        raise TypeError("Base argument must be a dictionary.")
    if not isinstance(override, dict):
        raise TypeError("Override argument must be a dictionary.")

    merged = base.copy()

    for key, override_value in override.items():
        if key in merged:
            base_value = merged[key]
            if isinstance(base_value, dict) and isinstance(override_value, dict):
                merged[key] = deep_merge(base_value, override_value)
            else:
                # If either side is not a dict, override value replaces base value
                merged[key] = override_value
        else:
            # Key only exists in override, add it
            merged[key] = override_value

    return merged
