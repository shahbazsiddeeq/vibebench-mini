def flatten_dict(d: dict, sep: str = ".") -> dict:
    result = {}

    def _flatten(obj, prefix):
        if isinstance(obj, dict) and obj:
            for key, value in obj.items():
                new_key = f"{prefix}{sep}{key}" if prefix else str(key)
                _flatten(value, new_key)
        else:
            # Leaf: a non-dict value, or an empty dict.
            if not prefix:
                # Only reachable when the whole input is an empty dict.
                return
            if prefix in result:
                raise ValueError(f"separator collision on key {prefix!r}")
            result[prefix] = obj

    _flatten(d, "")
    return result
