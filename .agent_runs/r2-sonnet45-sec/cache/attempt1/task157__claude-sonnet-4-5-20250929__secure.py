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
    # Validate input
    if not values:
        raise ValueError("values cannot be empty")
    
    # Ensure new_min and new_max are floats
    new_min = float(new_min)
    new_max = float(new_max)
    
    # Find min and max of input values
    lo = min(values)
    hi = max(values)
    
    # Special case: constant series (hi == lo)
    if hi == lo:
        # Return list where every element equals new_min
        return [round(new_min, 6) for _ in values]
    
    # Normal case: apply min-max normalization formula
    # scaled_value = new_min + (x - lo) / (hi - lo) * (new_max - new_min)
    result = []
    for x in values:
        scaled = new_min + (x - lo) / (hi - lo) * (new_max - new_min)
        result.append(round(scaled, 6))
    
    return result
