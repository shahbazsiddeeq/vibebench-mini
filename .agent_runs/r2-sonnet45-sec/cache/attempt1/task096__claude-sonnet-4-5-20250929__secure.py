def moving_average(data, window):
    """
    Calculate simple moving averages for the given data and window size.
    
    Args:
        data: A list of numeric values
        window: The size of the moving window (must be > 0 and <= len(data))
    
    Returns:
        A list of moving averages with length = len(data) - window + 1
    
    Raises:
        ValueError: If window <= 0 or window > len(data)
    """
    # Validate window parameter
    if not isinstance(window, int):
        raise ValueError("Window must be an integer")
    
    if window <= 0:
        raise ValueError("Window must be greater than 0")
    
    # Validate data parameter
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")
    
    if window > len(data):
        raise ValueError("Window size cannot be greater than data length")
    
    # Validate that all data elements are numeric
    try:
        # Convert to list if tuple and validate numeric types
        data_list = list(data)
        for item in data_list:
            if not isinstance(item, (int, float)) or isinstance(item, bool):
                raise ValueError("All data elements must be numeric")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid data: {e}")
    
    # Calculate moving averages
    result = []
    for i in range(len(data_list) - window + 1):
        window_sum = sum(data_list[i:i + window])
        avg = window_sum / window
        result.append(float(avg))
    
    return result
