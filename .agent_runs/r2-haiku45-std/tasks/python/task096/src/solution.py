def moving_average(data, window):
    """
    Calculate simple moving averages for the given data.
    
    Args:
        data: List of numbers
        window: Size of the moving window
        
    Returns:
        List of moving averages with length = len(data) - window + 1
        
    Raises:
        ValueError: if window <= 0 or window > len(data)
    """
    if window <= 0 or window > len(data):
        raise ValueError("window must be > 0 and <= len(data)")
    
    result = []
    for i in range(len(data) - window + 1):
        window_sum = sum(data[i:i + window])
        average = window_sum / window
        result.append(average)
    
    return result
