def expand_cases(base, overrides):
    """
    Expand a base dictionary with a list of override dictionaries.
    
    Returns a list with one new dict per override, where each result is base
    merged with that single override. The merge is SHALLOW - override values
    replace base values outright with no recursive merging.
    
    Args:
        base: A dictionary to use as the base for all results
        overrides: A list of dictionaries, each containing overrides to apply
        
    Returns:
        A list of new dictionaries, one per override, or empty list if overrides is empty
    """
    # Validate inputs
    if not isinstance(base, dict):
        raise TypeError("base must be a dictionary")
    if not isinstance(overrides, list):
        raise TypeError("overrides must be a list")
    
    result = []
    
    for override in overrides:
        if not isinstance(override, dict):
            raise TypeError("each override must be a dictionary")
        
        # Create a new dict by copying base
        merged = base.copy()
        
        # Apply the override (shallow merge - override values replace base values)
        merged.update(override)
        
        result.append(merged)
    
    return result
