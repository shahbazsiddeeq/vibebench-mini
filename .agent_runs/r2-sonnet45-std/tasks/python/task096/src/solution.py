def moving_average(data, window):
    """
    Calculate simple moving averages for the given data and window size.
    
    Args:
        data: List of numeric values
        window: Size of the moving window
        
    Returns:
        List of moving averages with length = len(data) - window + 1
        
    Raises:
        ValueError: If window <= 0 or window > len(data)
    """
    if window <= 0 or window > len(data):
        raise ValueError("Window must be positive and not greater than data length")
    
    result = []
    for i in range(len(data) - window + 1):
        window_data = data[i:i + window]
        avg = sum(window_data) / window
        result.append(avg)
    
    return result
