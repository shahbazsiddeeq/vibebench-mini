def deep_merge(base, override):
    """
    Recursively merges two dicts; override values take precedence;
    nested dicts are merged recursively, not replaced.
    When a key exists in both and either side is not a dict (including lists),
    the override value replaces the base value outright (lists are not concatenated).
    Returns a new top-level dict without modifying either input;
    nested dict values taken unchanged from base are shared (not deep-copied) with base.
    """
    if not isinstance(base, dict) or not isinstance(override, dict):
        # If either is not a dict, override replaces base
        return override

    merged = dict(base)  # Start with a shallow copy of base

    for key, override_value in override.items():
        if key in merged:
            base_value = merged[key]
            if isinstance(base_value, dict) and isinstance(override_value, dict):
                # Both are dicts, recurse
                merged[key] = deep_merge(base_value, override_value)
            else:
                # One or both are not dicts, override replaces base
                merged[key] = override_value
        else:
            # Key only in override, add it
            merged[key] = override_value

    return merged
