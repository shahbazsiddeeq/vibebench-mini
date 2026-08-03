"""Percentile calculator module."""


def percentile(data, p):
    """
    Calculate the pth percentile of data using linear interpolation.
    
    Args:
        data: A sequence of numeric values
        p: Percentile value (0-100)
        
    Returns:
        The pth percentile as a float
        
    Raises:
        ValueError: If data is empty or p is outside [0, 100]
    """
    # Validate inputs
    if not data:
        raise ValueError("data cannot be empty")
    
    if not isinstance(p, (int, float)) or p < 0 or p > 100:
        raise ValueError("p must be a number between 0 and 100")
    
    # Validate that data contains numeric values
    try:
        sorted_data = sorted(float(x) for x in data)
    except (TypeError, ValueError):
        raise ValueError("data must contain numeric values")
    
    n = len(sorted_data)
    
    # Handle edge cases
    if p == 0:
        return sorted_data[0]
    if p == 100:
        return sorted_data[-1]
    
    # Linear interpolation method
    # Position in the sorted array (0-indexed)
    # Using the formula: position = (p/100) * (n - 1)
    position = (p / 100.0) * (n - 1)
    
    # Get the lower and upper indices
    lower_index = int(position)
    upper_index = lower_index + 1
    
    # If position is exact integer, return that value
    if position == lower_index:
        return sorted_data[lower_index]
    
    # Linear interpolation between two values
    fraction = position - lower_index
    lower_value = sorted_data[lower_index]
    upper_value = sorted_data[upper_index]
    
    result = lower_value + fraction * (upper_value - lower_value)
    return result
