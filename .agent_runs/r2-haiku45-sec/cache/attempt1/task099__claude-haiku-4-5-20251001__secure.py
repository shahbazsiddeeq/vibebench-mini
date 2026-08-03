"""
Outlier detection module using z-score analysis.
"""

import math
from typing import List, Union


def find_outliers(data: List[Union[int, float]], z_threshold: float = 2.5) -> List[Union[int, float]]:
    """
    Find outliers in data based on z-score using population standard deviation.
    
    Args:
        data: List of numeric values to analyze
        z_threshold: Threshold for absolute z-score (default 2.5)
        
    Returns:
        List of outlier values in their original order
        
    Raises:
        ValueError: If data has fewer than 2 elements
    """
    # Input validation
    if not isinstance(data, list):
        raise ValueError("Data must be a list")
    
    if len(data) < 2:
        raise ValueError("Need at least 2 elements")
    
    # Validate all elements are numeric
    try:
        numeric_data = [float(x) for x in data]
    except (TypeError, ValueError):
        raise ValueError("All elements must be numeric")
    
    # Validate z_threshold is numeric
    try:
        z_threshold = float(z_threshold)
    except (TypeError, ValueError):
        raise ValueError("z_threshold must be numeric")
    
    # Calculate mean
    mean = sum(numeric_data) / len(numeric_data)
    
    # Calculate population standard deviation
    # variance = mean of squared deviations (divide by N, not N-1)
    squared_deviations = [(x - mean) ** 2 for x in numeric_data]
    variance = sum(squared_deviations) / len(numeric_data)
    std_dev = math.sqrt(variance)
    
    # If standard deviation is 0, return empty list
    if std_dev == 0:
        return []
    
    # Find outliers: values with |z-score| > z_threshold
    outliers = []
    for value in numeric_data:
        z_score = (value - mean) / std_dev
        if abs(z_score) > z_threshold:
            outliers.append(value)
    
    return outliers
