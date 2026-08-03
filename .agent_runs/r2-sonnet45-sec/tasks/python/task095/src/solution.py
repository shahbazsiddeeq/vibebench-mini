def percentile(data, p):
    """
    Calculate the pth percentile of data using linear interpolation.
    
    Args:
        data: A list or sequence of numeric values
        p: Percentile value between 0 and 100 (inclusive)
    
    Returns:
        The pth percentile as a float
    
    Raises:
        ValueError: If data is empty or p is outside [0, 100]
    """
    # Validate inputs
    if not isinstance(p, (int, float)):
        raise ValueError("Percentile must be a number")
    
    if p < 0 or p > 100:
        raise ValueError("Percentile must be between 0 and 100")
    
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Validate data contains only numbers
    try:
        sorted_data = sorted(float(x) for x in data)
    except (TypeError, ValueError):
        raise ValueError("Data must contain only numeric values")
    
    n = len(sorted_data)
    
    # Handle edge cases
    if n == 1:
        return float(sorted_data[0])
    
    # Calculate the position using linear interpolation formula
    # Position = (p/100) * (n - 1)
    position = (p / 100.0) * (n - 1)
    
    # Get the lower and upper indices
    lower_index = int(position)
    upper_index = lower_index + 1
    
    # If position is exactly on an index, return that value
    if position == lower_index:
        return float(sorted_data[lower_index])
    
    # If upper_index is beyond the array, return the last element
    if upper_index >= n:
        return float(sorted_data[-1])
    
    # Linear interpolation between the two values
    fraction = position - lower_index
    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]
    
    result = lower_value + fraction * (upper_value - lower_value)
    
    return float(result)
