def weighted_average(values, weights):
    """
    Calculate the weighted arithmetic mean of values using weights.
    
    Args:
        values: List of numbers (ints or floats)
        weights: List of numbers (ints or floats)
    
    Returns:
        float: Weighted average rounded to 6 decimal places
    
    Raises:
        ValueError: If values is empty, weights is empty, lists have different
                   lengths, or sum of weights is zero
    """
    # Check if either list is empty
    if not values:
        raise ValueError("values cannot be empty")
    if not weights:
        raise ValueError("weights cannot be empty")
    
    # Check if lists have different lengths
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    
    # Calculate sum of weights
    total_weight = sum(weights)
    
    # Check if sum of weights is zero
    if total_weight == 0:
        raise ValueError("sum of weights cannot be zero")
    
    # Calculate weighted sum
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    
    # Calculate and return weighted average rounded to 6 decimal places
    result = weighted_sum / total_weight
    return round(result, 6)
