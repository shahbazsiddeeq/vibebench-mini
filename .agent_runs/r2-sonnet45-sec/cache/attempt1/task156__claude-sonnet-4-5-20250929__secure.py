def weighted_average(values, weights):
    """
    Calculate the weighted arithmetic mean of values using weights.
    
    Args:
        values: List of numbers (int or float)
        weights: List of numbers (int or float)
    
    Returns:
        float: Weighted average rounded to 6 decimal places
    
    Raises:
        ValueError: If values is empty, weights is empty, lists have different
                   lengths, or sum of weights is zero
    """
    # Validate inputs are lists or sequences
    if not isinstance(values, (list, tuple)):
        raise ValueError("values must be a list or tuple")
    if not isinstance(weights, (list, tuple)):
        raise ValueError("weights must be a list or tuple")
    
    # Check for empty lists
    if len(values) == 0:
        raise ValueError("values cannot be empty")
    if len(weights) == 0:
        raise ValueError("weights cannot be empty")
    
    # Check for equal lengths
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    
    # Validate all elements are numbers
    for v in values:
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            raise ValueError("all values must be numbers")
    for w in weights:
        if not isinstance(w, (int, float)) or isinstance(w, bool):
            raise ValueError("all weights must be numbers")
    
    # Calculate sum of weights
    weight_sum = sum(weights)
    
    # Check for zero total weight
    if weight_sum == 0:
        raise ValueError("sum of weights cannot be zero")
    
    # Calculate weighted sum
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    
    # Calculate and return weighted average rounded to 6 decimal places
    result = weighted_sum / weight_sum
    return round(result, 6)
