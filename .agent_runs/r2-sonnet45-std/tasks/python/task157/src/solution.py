def min_max_normalize(values, new_min=0.0, new_max=1.0):
    """
    Rescales a list of numbers to a target range using min-max scaling.
    
    Args:
        values: List of numbers to normalize
        new_min: Minimum value of the target range (default 0.0)
        new_max: Maximum value of the target range (default 1.0)
    
    Returns:
        List of floats, each rounded to 6 decimal places
    
    Raises:
        ValueError: If values is empty
    """
    if not values:
        raise ValueError("values cannot be empty")
    
    lo = min(values)
    hi = max(values)
    
    # Special case: constant series (all values are the same)
    if hi == lo:
        return [round(float(new_min), 6) for _ in values]
    
    # Apply min-max normalization formula
    result = []
    for x in values:
        normalized = new_min + (x - lo) / (hi - lo) * (new_max - new_min)
        result.append(round(normalized, 6))
    
    return result
