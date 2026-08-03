def moving_average(data, window):
    """
    Calculate simple moving averages for the given data.
    
    Args:
        data: List of numeric values
        window: Size of the moving window (must be > 0 and <= len(data))
    
    Returns:
        List of moving averages with length = len(data) - window + 1
    
    Raises:
        ValueError: If window <= 0 or window > len(data)
    """
    # Input validation
    if not isinstance(window, int) or window <= 0:
        raise ValueError("window must be a positive integer")
    
    if window > len(data):
        raise ValueError("window cannot be larger than data length")
    
    # Validate data is iterable and contains numeric values
    try:
        data_list = list(data)
    except TypeError:
        raise ValueError("data must be iterable")
    
    if not data_list:
        raise ValueError("data cannot be empty")
    
    # Validate all elements are numeric
    try:
        for item in data_list:
            float(item)
    except (TypeError, ValueError):
        raise ValueError("all data elements must be numeric")
    
    # Calculate moving averages
    result = []
    for i in range(len(data_list) - window + 1):
        window_sum = sum(data_list[i:i + window])
        average = window_sum / window
        result.append(float(average))
    
    return result
