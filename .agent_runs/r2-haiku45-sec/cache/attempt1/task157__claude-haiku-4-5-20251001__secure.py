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
    # Input validation
    if not isinstance(values, (list, tuple)):
        raise ValueError("values must be a list or tuple")
    
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    # Validate that all elements are numbers
    try:
        numeric_values = [float(v) for v in values]
    except (TypeError, ValueError):
        raise ValueError("all elements in values must be numeric")
    
    # Validate new_min and new_max are numbers
    try:
        new_min = float(new_min)
        new_max = float(new_max)
    except (TypeError, ValueError):
        raise ValueError("new_min and new_max must be numeric")
    
    # Find min and max of the input values
    lo = min(numeric_values)
    hi = max(numeric_values)
    
    # Handle constant series (hi == lo)
    if hi == lo:
        return [round(float(new_min), 6) for _ in numeric_values]
    
    # Calculate the scaling factor
    span = hi - lo
    new_span = new_max - new_min
    
    # Apply min-max normalization formula to each value
    result = []
    for x in numeric_values:
        scaled = new_min + (x - lo) / span * new_span
        result.append(round(scaled, 6))
    
    return result
