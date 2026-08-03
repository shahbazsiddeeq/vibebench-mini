# src/solution.py

def deep_merge(base, override):
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise ValueError("Both base and override must be dictionaries.")

    merged = base.copy()  # Start with a shallow copy of the base

    for key, override_value in override.items():
        if key in merged:
            base_value = merged[key]
            if isinstance(base_value, dict) and isinstance(override_value, dict):
                # Recursively merge dictionaries
                merged[key] = deep_merge(base_value, override_value)
            else:
                # Override with the new value
                merged[key] = override_value
        else:
            # If the key is not in base, just add it
            merged[key] = override_value

    return merged
