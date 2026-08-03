def find_outliers(data, z_threshold=2.5):
    """
    Find outliers in data based on z-score threshold.
    
    Args:
        data: List of numeric values
        z_threshold: Threshold for absolute z-score (default 2.5)
    
    Returns:
        List of values whose absolute z-score is strictly greater than z_threshold,
        in their original order.
    
    Raises:
        ValueError: If data has fewer than 2 elements
    """
    # Validate input
    if not isinstance(data, (list, tuple)):
        raise ValueError("Data must be a list or tuple")
    
    if len(data) < 2:
        raise ValueError("Data must contain at least 2 elements")
    
    # Validate that all elements are numeric
    try:
        numeric_data = [float(x) for x in data]
    except (TypeError, ValueError):
        raise ValueError("All data elements must be numeric")
    
    # Validate z_threshold
    try:
        z_threshold = float(z_threshold)
    except (TypeError, ValueError):
        raise ValueError("z_threshold must be numeric")
    
    # Calculate mean
    n = len(numeric_data)
    mean = sum(numeric_data) / n
    
    # Calculate population variance (divide by N, not N-1)
    squared_deviations = [(x - mean) ** 2 for x in numeric_data]
    variance = sum(squared_deviations) / n
    
    # If variance is 0, standard deviation is 0, return empty list
    if variance == 0:
        return []
    
    # Calculate standard deviation
    std_dev = variance ** 0.5
    
    # Calculate z-scores and find outliers
    outliers = []
    for i, value in enumerate(numeric_data):
        z_score = (value - mean) / std_dev
        if abs(z_score) > z_threshold:
            # Return original value from data, not converted float
            outliers.append(data[i])
    
    return outliers
