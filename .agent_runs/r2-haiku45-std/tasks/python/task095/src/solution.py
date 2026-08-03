def percentile(data, p):
    """
    Calculate the pth percentile of data using linear interpolation.
    
    Args:
        data: A list of numeric values
        p: The percentile to calculate (0-100)
    
    Returns:
        The pth percentile value
    
    Raises:
        ValueError: If data is empty or p is outside 0-100
    """
    if not data:
        raise ValueError("data cannot be empty")
    
    if p < 0 or p > 100:
        raise ValueError("p must be between 0 and 100")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    # Calculate the index for the percentile
    # Using the linear interpolation method
    index = (p / 100.0) * (n - 1)
    
    # Get the lower and upper indices
    lower_index = int(index)
    upper_index = lower_index + 1
    
    # If index is an integer, return the value at that index
    if index == lower_index:
        return float(sorted_data[lower_index])
    
    # Otherwise, interpolate between the two values
    if upper_index >= n:
        return float(sorted_data[lower_index])
    
    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]
    fraction = index - lower_index
    
    return lower_value + fraction * (upper_value - lower_value)
