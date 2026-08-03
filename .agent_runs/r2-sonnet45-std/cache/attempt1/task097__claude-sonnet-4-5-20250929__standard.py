def z_scores(data):
    """
    Calculate z-scores for each element in the data.
    
    Args:
        data: A list or sequence of numeric values
        
    Returns:
        A list of z-scores (x - mean) / std for each element
        
    Raises:
        ValueError: If len(data) < 2 or std == 0
    """
    if len(data) < 2:
        raise ValueError("Data must contain at least 2 elements")
    
    # Calculate mean
    mean = sum(data) / len(data)
    
    # Calculate population standard deviation (ddof=0)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = variance ** 0.5
    
    if std == 0:
        raise ValueError("Standard deviation is zero")
    
    # Calculate z-scores
    return [(x - mean) / std for x in data]
