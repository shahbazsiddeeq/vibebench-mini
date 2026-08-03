def min_max_normalize(values, new_min=0.0, new_max=1.0):
    """
    Rescales a list of numbers to a target range using min-max scaling.
    
    Args:
        values: List of numbers to normalize
        new_min: Minimum value of the target range (default 0.0)
        new_max: Maximum value of the target range (default 1.0)
    
    Returns:
        A new list of floats, each rounded to 6 decimal places
    
    Raises:
        ValueError: If values is empty
    """
    if not values:
        raise ValueError("values cannot be empty")
    
    lo = min(values)
    hi = max(values)
    
    # Special case: constant series (hi == lo)
    if hi == lo:
        return [round(float(new_min), 6) for _ in values]
    
    # General case: scale each value
    result = []
    span = hi - lo
    new_span = new_max - new_min
    
    for x in values:
        scaled = new_min + (x - lo) / span * new_span
        result.append(round(scaled, 6))
    
    return result
