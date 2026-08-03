def flatten(nested):
    """
    Recursively flattens arbitrarily deep nested lists into a single flat list.
    Non-list items pass through unchanged.
    
    Args:
        nested: A potentially nested list structure
        
    Returns:
        A flat list containing all non-list elements from the nested structure
    """
    result = []
    
    # Handle None input
    if nested is None:
        return result
    
    # Validate input is iterable (but not string, which is also iterable)
    if isinstance(nested, str):
        return [nested]
    
    # Check if input is iterable
    try:
        iter(nested)
    except TypeError:
        # If not iterable, return it as a single-element list
        return [nested]
    
    for item in nested:
        # Check if item is a list (or list-like, but not string)
        if isinstance(item, list):
            # Recursively flatten the nested list
            result.extend(flatten(item))
        elif isinstance(item, str):
            # Strings are iterable but should be treated as atomic items
            result.append(item)
        else:
            # Check if it's another iterable type (tuple, etc.)
            try:
                # Try to iterate, but avoid strings
                iter(item)
                # If it's iterable and not a string, flatten it
                result.extend(flatten(item))
            except TypeError:
                # Not iterable, just append
                result.append(item)
    
    return result
