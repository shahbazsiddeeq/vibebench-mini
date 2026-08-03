def flatten(nested):
    """
    Recursively flattens arbitrarily deep nested lists into a single flat list.
    Non-list items pass through unchanged.
    
    Args:
        nested: A potentially nested list structure
        
    Returns:
        A flattened list containing all non-list items
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
