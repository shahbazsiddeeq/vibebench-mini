def flatten(nested):
    """
    Recursively flattens arbitrarily deep nested lists into a single flat list.
    Non-list items pass through unchanged.
    
    Args:
        nested: A list that may contain nested lists and other items
        
    Returns:
        A flattened list containing all non-list items in order
        
    Raises:
        TypeError: If nested is not a list
    """
    if not isinstance(nested, list):
        raise TypeError("Input must be a list")
    
    result = []
    
    for item in nested:
        if isinstance(item, list):
            # Recursively flatten nested lists
            result.extend(flatten(item))
        else:
            # Add non-list items directly
            result.append(item)
    
    return result
