def weighted_average(values, weights):
    """
    Calculate the weighted arithmetic mean of values using weights.
    
    Args:
        values: List of numbers (ints or floats)
        weights: List of numbers (ints or floats)
    
    Returns:
        float: The weighted average rounded to 6 decimal places
    
    Raises:
        ValueError: If values is empty, weights is empty, lengths differ,
                   or sum of weights is zero
    """
    # Check if values is empty
    if not values:
        raise ValueError("values list is empty")
    
    # Check if weights is empty
    if not weights:
        raise ValueError("weights list is empty")
    
    # Check if lengths are different
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    
    # Calculate sum of weights
    total_weight = sum(weights)
    
    # Check if sum of weights is zero
    if total_weight == 0:
        raise ValueError("sum of weights cannot be zero")
    
    # Calculate weighted sum
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    
    # Calculate and return the weighted average rounded to 6 decimal places
    result = weighted_sum / total_weight
    return round(result, 6)
