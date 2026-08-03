import statistics
from typing import List, Union


def z_scores(data: List[Union[int, float]]) -> List[float]:
    """
    Calculate z-scores for each element in the data.
    
    Z-score is calculated as (x - mean) / std, where std is the population
    standard deviation (ddof=0).
    
    Args:
        data: A list of numeric values
        
    Returns:
        A list of z-scores (floats) for each element
        
    Raises:
        ValueError: If len(data) < 2 or if standard deviation is 0
    """
    # Validate input
    if not isinstance(data, list):
        raise ValueError("Input must be a list")
    
    if len(data) < 2:
        raise ValueError("Data must contain at least 2 elements")
    
    # Validate all elements are numeric
    try:
        numeric_data = [float(x) for x in data]
    except (TypeError, ValueError):
        raise ValueError("All elements must be numeric")
    
    # Calculate mean
    mean = statistics.mean(numeric_data)
    
    # Calculate population standard deviation (ddof=0)
    # Using the formula: sqrt(sum((x - mean)^2) / n)
    variance = sum((x - mean) ** 2 for x in numeric_data) / len(numeric_data)
    std = variance ** 0.5
    
    # Check if standard deviation is zero
    if std == 0:
        raise ValueError("Standard deviation cannot be zero")
    
    # Calculate and return z-scores
    return [(x - mean) / std for x in numeric_data]
