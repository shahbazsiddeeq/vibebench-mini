def percentile(data, p):
    """
    Calculate the pth percentile of data using linear interpolation.
    
    Args:
        data: A list of numeric values
        p: Percentile value between 0 and 100 (inclusive)
    
    Returns:
        The pth percentile value
    
    Raises:
        ValueError: If data is empty or p is outside [0, 100]
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    if p < 0 or p > 100:
        raise ValueError("Percentile must be between 0 and 100")
    
    # Sort the data
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    # Handle edge cases
    if p == 0:
        return sorted_data[0]
    if p == 100:
        return sorted_data[-1]
    
    # Calculate position using linear interpolation
    position = (p / 100) * (n - 1)
    
    # Get the lower and upper indices
    lower_index = int(position)
    upper_index = lower_index + 1
    
    # If position is exactly an integer, return that element
    if position == lower_index:
        return float(sorted_data[lower_index])
    
    # Otherwise, interpolate between the two values
    fraction = position - lower_index
    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]
    
    return lower_value + fraction * (upper_value - lower_value)
