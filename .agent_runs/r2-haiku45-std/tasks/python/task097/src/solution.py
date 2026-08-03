import statistics
from typing import List, Union

def z_scores(data: List[Union[int, float]]) -> List[float]:
    """
    Calculate z-scores for each element in the data.
    
    Z-score is calculated as (x - mean) / std, where std is the population 
    standard deviation (ddof=0).
    
    Args:
        data: List of numeric values
        
    Returns:
        List of z-scores for each element
        
    Raises:
        ValueError: if len(data) < 2 or if standard deviation is 0
    """
    if len(data) < 2:
        raise ValueError("Data must have at least 2 elements")
    
    # Calculate mean
    mean = statistics.mean(data)
    
    # Calculate population standard deviation (ddof=0)
    # Population variance: sum((x - mean)^2) / n
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = variance ** 0.5
    
    if std == 0:
        raise ValueError("Standard deviation cannot be zero")
    
    # Calculate z-scores
    return [(x - mean) / std for x in data]
