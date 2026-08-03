def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge two dictionaries without modifying either input."""
    result = base.copy()

    for key, override_value in override.items():
        base_value = base.get(key)

        if key in base and isinstance(base_value, dict) and isinstance(override_value, dict):
            result[key] = deep_merge(base_value, override_value)
        else:
            result[key] = override_value

    return result
