import math


def z_scores(data):
    """
    Calculate z-scores for each element in the data.
    
    Z-score is calculated as (x - mean) / std, where std is the population
    standard deviation (ddof=0).
    
    Args:
        data: A list or sequence of numeric values
        
    Returns:
        A list of z-scores corresponding to each element in data
        
    Raises:
        ValueError: If len(data) < 2 or if std == 0
    """
    # Validate input
    if not isinstance(data, (list, tuple)):
        try:
            data = list(data)
        except (TypeError, ValueError):
            raise ValueError("Data must be a sequence of numeric values")
    
    # Check minimum length
    if len(data) < 2:
        raise ValueError("Data must contain at least 2 elements")
    
    # Validate all elements are numeric
    try:
        numeric_data = [float(x) for x in data]
    except (TypeError, ValueError):
        raise ValueError("All elements in data must be numeric")
    
    # Calculate mean
    n = len(numeric_data)
    mean = sum(numeric_data) / n
    
    # Calculate population standard deviation (ddof=0)
    variance = sum((x - mean) ** 2 for x in numeric_data) / n
    std = math.sqrt(variance)
    
    # Check if standard deviation is zero
    if std == 0.0:
        raise ValueError("Standard deviation is zero")
    
    # Calculate z-scores
    result = [(x - mean) / std for x in numeric_data]
    
    return result
