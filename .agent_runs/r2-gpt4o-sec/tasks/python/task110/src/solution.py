def deep_merge(base, override):
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise TypeError("Both base and override must be dictionaries.")

    def merge_dicts(d1, d2):
        result = d1.copy()
        for key, value in d2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dicts(result[key], value)
            else:
                result[key] = value
        return result

    return merge_dicts(base, override)
