def find_outliers(data, z_threshold=2.5):
    """
    Find outliers in data based on z-score threshold.
    
    Args:
        data: List of numeric values
        z_threshold: Threshold for absolute z-score (default 2.5)
    
    Returns:
        List of values whose absolute z-score is strictly greater than z_threshold
    
    Raises:
        ValueError: If data has fewer than 2 elements
    """
    if len(data) < 2:
        raise ValueError("Need at least 2 data points")
    
    # Calculate mean
    mean = sum(data) / len(data)
    
    # Calculate population variance (divide by N)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    
    # Calculate population standard deviation
    std = variance ** 0.5
    
    # If std is 0, all values are the same, no outliers
    if std == 0:
        return []
    
    # Find outliers: values whose absolute z-score > z_threshold
    outliers = []
    for value in data:
        z_score = abs((value - mean) / std)
        if z_score > z_threshold:
            outliers.append(value)
    
    return outliers
