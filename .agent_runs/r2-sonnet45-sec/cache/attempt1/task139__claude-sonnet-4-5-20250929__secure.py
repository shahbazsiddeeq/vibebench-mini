def expand_cases(base, overrides):
    """
    Expand test cases by merging base dict with each override dict.
    
    Args:
        base: A dictionary containing base values
        overrides: A list of dictionaries, each containing override values
    
    Returns:
        A list of dictionaries, where each result is a shallow merge of base
        with one override dict. Override values win on key collisions.
        Returns empty list if overrides is empty.
    """
    # Validate inputs
    if not isinstance(base, dict):
        raise TypeError("base must be a dictionary")
    if not isinstance(overrides, list):
        raise TypeError("overrides must be a list")
    
    # Validate all items in overrides are dictionaries
    for i, override in enumerate(overrides):
        if not isinstance(override, dict):
            raise TypeError(f"overrides[{i}] must be a dictionary")
    
    # Return empty list if no overrides
    if not overrides:
        return []
    
    result = []
    for override in overrides:
        # Create a shallow copy of base
        merged = base.copy()
        # Update with override (shallow merge - override values replace base values)
        merged.update(override)
        result.append(merged)
    
    return result
