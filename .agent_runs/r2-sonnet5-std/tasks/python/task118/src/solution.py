# src/solution.py

def flatten_dict(d, sep="."):
    """
    Flatten a nested dictionary into a single-level dict with keys joined by `sep`.

    - A non-dict value is a leaf.
    - An empty dict is a leaf too, but preserved as `{}` in the output.
    - If two different original paths collapse to the same flattened key,
      raises ValueError.
    """
    if not isinstance(d, dict):
        raise TypeError("flatten_dict expects a dict")

    result = {}

    def _flatten(current, prefix_parts):
        if isinstance(current, dict) and len(current) == 0:
            key = sep.join(prefix_parts)
            _set(key, {})
            return
        if isinstance(current, dict):
            for k, v in current.items():
                _flatten(v, prefix_parts + [str(k)])
        else:
            key = sep.join(prefix_parts)
            _set(key, current)

    def _set(key, value):
        if key in result:
            raise ValueError(f"Key collision detected for flattened key: '{key}'")
        result[key] = value

    if len(d) == 0:
        return {}

    for k, v in d.items():
        _flatten(v, [str(k)])

    return result
