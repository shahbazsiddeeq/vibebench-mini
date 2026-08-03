def weighted_average(values, weights):
    """
    Calculate the weighted arithmetic mean of values using weights.
    
    Args:
        values: List of numbers (ints or floats)
        weights: List of numbers (ints or floats) to weight the values
        
    Returns:
        float: The weighted average rounded to 6 decimal places
        
    Raises:
        ValueError: If values is empty, weights is empty, lengths differ,
                   or sum of weights equals zero
    """
    # Validate inputs are lists/sequences
    if not isinstance(values, (list, tuple)):
        raise ValueError("values must be a list or tuple")
    if not isinstance(weights, (list, tuple)):
        raise ValueError("weights must be a list or tuple")
    
    # Check if values is empty
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    
    # Check if weights is empty
    if len(weights) == 0:
        raise ValueError("weights cannot be empty")
    
    # Check if lengths match
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    
    # Validate that all elements are numbers
    try:
        values_float = [float(v) for v in values]
        weights_float = [float(w) for w in weights]
    except (TypeError, ValueError):
        raise ValueError("All values and weights must be numbers")
    
    # Calculate sum of weights
    sum_weights = sum(weights_float)
    
    # Check if sum of weights is zero
    if sum_weights == 0:
        raise ValueError("sum of weights cannot be zero")
    
    # Calculate weighted sum
    weighted_sum = sum(v * w for v, w in zip(values_float, weights_float))
    
    # Calculate and return the weighted average rounded to 6 decimal places
    result = weighted_sum / sum_weights
    return round(result, 6)
