def find_outliers(data, z_threshold=2.5):
    """
    Find outliers in data based on z-score.
    
    Returns the list of values whose absolute z-score is strictly greater than z_threshold,
    in their original order.
    
    Uses population standard deviation (divide by N).
    
    Args:
        data: List of numeric values
        z_threshold: Z-score threshold (default 2.5)
    
    Returns:
        List of outlier values in original order
    
    Raises:
        ValueError: If data has fewer than 2 elements
    """
    if len(data) < 2:
        raise ValueError("Need at least 2 elements")
    
    # Calculate mean
    mean = sum(data) / len(data)
    
    # Calculate population standard deviation
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5
    
    # If standard deviation is 0, return empty list
    if std_dev == 0:
        return []
    
    # Find outliers
    outliers = []
    for value in data:
        z_score = abs((value - mean) / std_dev)
        if z_score > z_threshold:
            outliers.append(value)
    
    return outliers
