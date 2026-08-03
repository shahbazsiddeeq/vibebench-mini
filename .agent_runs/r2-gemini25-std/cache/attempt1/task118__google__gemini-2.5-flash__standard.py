def flatten_dict(d, sep="."):
    """
    Flattens a nested dictionary into a single-level dict with keys joined by sep.

    A non-dict value, or an empty dict, is treated as a leaf; an empty dict is
    preserved as its joined key mapping to {} (e.g. {"a": {}} -> {"a": {}}).
    If two different paths collapse to the same flattened key (a separator collision),
    raises ValueError. An empty top-level dict returns {}.

    Args:
        d (dict): The dictionary to flatten.
        sep (str): The separator to use for joining keys.

    Returns:
        dict: The flattened dictionary.

    Raises:
        ValueError: If a separator collision occurs (two different paths collapse
                    to the same flattened key).
    """
    if not isinstance(d, dict):
        raise TypeError("Input must be a dictionary.")

    flattened = {}
    
    def _flatten_recursive(current_dict, current_key_path):
        for key, value in current_dict.items():
            new_key_path = f"{current_key_path}{sep}{key}" if current_key_path else key

            if isinstance(value, dict) and value:  # Non-empty dict, recurse
                _flatten_recursive(value, new_key_path)
            else:  # Leaf node (non-dict value or empty dict)
                if new_key_path in flattened:
                    # Check for collision: if the key already exists, it means
                    # two different paths led to the same flattened key.
                    raise ValueError(f"Separator collision: '{new_key_path}' already exists.")
                flattened[new_key_path] = value

    _flatten_recursive(d, "")
    return flattened
