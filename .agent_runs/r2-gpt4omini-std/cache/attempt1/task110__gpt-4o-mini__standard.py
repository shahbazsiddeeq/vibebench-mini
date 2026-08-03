# src/solution.py

def deep_merge(base, override):
    result = base.copy()  # Start with a shallow copy of the base dict

    for key, value in override.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                # Both are dicts, merge them recursively
                result[key] = deep_merge(result[key], value)
            else:
                # Override with the new value
                result[key] = value
        else:
            # Key is not in base, add it
            result[key] = value

    return result
