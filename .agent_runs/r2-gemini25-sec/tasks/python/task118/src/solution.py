import collections

def flatten_dict(d, sep="."):
    """
    Flattens a nested dictionary into a single-level dict with keys joined by sep.

    A non-dict value, or an empty dict, is treated as a leaf; an empty dict is
    preserved as its joined key mapping to {} (e.g. {"a": {}} -> {"a": {}}).
    If two different paths collapse to the same flattened key (a separator collision),
    raises ValueError. An empty top-level dict returns {}.

    Args:
        d (dict): The dictionary to flatten.
        sep (str): The separator string to join keys.

    Returns:
        dict: The flattened dictionary.

    Raises:
        TypeError: If d is not a dictionary.
        TypeError: If sep is not a string.
        ValueError: If a separator collision occurs (two different paths
                    collapse to the same flattened key).
    """
    if not isinstance(d, dict):
        raise TypeError("Input 'd' must be a dictionary.")
    if not isinstance(sep, str):
        raise TypeError("Input 'sep' must be a string.")

    if not d:
        return {}

    flattened = {}
    
    # Use a deque for BFS-like traversal to avoid deep recursion and potential stack overflow
    # Each item in the queue is a tuple: (current_dict, current_prefix_parts)
    queue = collections.deque([(d, [])])

    while queue:
        current_dict, prefix_parts = queue.popleft()

        for key, value in current_dict.items():
            if not isinstance(key, (str, int, float)): # Basic validation for key types
                raise TypeError(f"Dictionary key '{key}' is of an unsupported type. Keys must be strings, integers, or floats.")
            
            # Convert key to string for joining, ensuring consistent behavior
            str_key = str(key)

            new_prefix_parts = prefix_parts + [str_key]
            flattened_key = sep.join(new_prefix_parts)

            if isinstance(value, dict) and value:  # If it's a non-empty dictionary, continue flattening
                queue.append((value, new_prefix_parts))
            else:  # It's a leaf node (non-dict value or an empty dict)
                if flattened_key in flattened:
                    # Collision detection: if the key already exists, check if the value is different.
                    # If values are different, it's a collision.
                    # If values are the same, it's redundant but not a collision in the sense of conflicting paths.
                    # The problem statement implies "two different paths collapse to the same flattened key"
                    # which means if we arrive at the same key from different paths, it's a collision.
                    # Since we are building the dict, if a key is already present, it means a previous path
                    # already defined it. If the current path also defines it, and the value is different,
                    # it's a collision. If the value is the same, it's effectively the same path.
                    # However, the strict interpretation of "two different paths" means any re-definition
                    # of an existing key from a new path is a collision.
                    # For simplicity and security, we'll treat any attempt to overwrite an existing key
                    # as a potential collision if it originates from a new traversal.
                    # A more robust collision check would involve storing the full path for each key,
                    # but given the problem statement, a simple check for existence is sufficient
                    # to catch most common collision scenarios.
                    # The problem implies that if `{"a": {"b": 1}}` and `{"a.b": 2}` were somehow merged,
                    # it would be a collision. Here, we are flattening a single dict.
                    # A collision would typically arise from malformed input like
                    # `{"a": {"b": 1}, "a.b": 2}` if the `sep` was `.` and `a.b` was treated as a literal key.
                    # Our current logic correctly handles `{"a": {"b": 1}, "a.b": 2}` as `{"a.b": 2}`
                    # if `a.b` is a top-level key.
                    # The specific wording "If two different paths collapse to the same flattened key"
                    # suggests that if `{"a": {"b": 1}}` and `{"a_b": 2}` were flattened with `_` as sep,
                    # and `a_b` was also a key, it would be a collision.
                    # Our current approach ensures that each unique flattened_key is assigned only once.
                    # If a key is generated multiple times from different paths, it implies a collision.
                    # For example, if `sep` is `.` and we have `{"a": {"b": 1}, "a.b": 2}`,
                    # the first path `a.b` would map to 1. The second path `a.b` would map to 2.
                    # This is a collision.
                    # The current implementation will overwrite, which is not what the problem asks.
                    # We need to detect if a key is *already present* from a *different logical path*.
                    # The simplest way to detect this is to check if the key already exists.
                    # If it exists, and we are about to assign a new value, it's a collision.
                    # This assumes that the input dictionary itself doesn't have keys that
                    # are already flattened versions of other nested keys.
                    # Example: {"a": {"b": 1}, "a.b": 2} -> This is a collision.
                    # Our current logic would process "a.b": 1 first, then "a.b": 2, overwriting.
                    # To detect collision, we must check if `flattened_key` is already in `flattened`.
                    # If it is, and we are about to assign a new value, it's a collision.
                    raise ValueError(f"Separator collision detected: flattened key '{flattened_key}' already exists.")
                flattened[flattened_key] = value

    return flattened
