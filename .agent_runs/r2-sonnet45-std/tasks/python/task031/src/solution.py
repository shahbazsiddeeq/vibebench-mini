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
    
    for item in nested:
        if isinstance(item, list):
            # Recursively flatten nested lists
            result.extend(flatten(item))
        else:
            # Add non-list items directly
            result.append(item)
    
    return result
