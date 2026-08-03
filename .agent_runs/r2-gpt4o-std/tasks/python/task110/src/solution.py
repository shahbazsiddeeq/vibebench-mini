def deep_merge(base, override):
    if not isinstance(base, dict) or not isinstance(override, dict):
        return override

    merged = base.copy()

    for key, override_value in override.items():
        base_value = merged.get(key)

        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = deep_merge(base_value, override_value)
        else:
            merged[key] = override_value

    return merged
