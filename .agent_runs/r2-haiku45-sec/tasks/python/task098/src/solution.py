"""
Pearson Correlation Coefficient Calculator

This module provides a secure implementation of the Pearson correlation coefficient.
"""

from typing import Union, List


def pearson_r(x: Union[List[float], List[int]], y: Union[List[float], List[int]]) -> float:
    """
    Calculate the Pearson correlation coefficient between two sequences.
    
    Args:
        x: First sequence of numeric values
        y: Second sequence of numeric values
        
    Returns:
        Pearson correlation coefficient rounded to 4 decimal places
        
    Raises:
        ValueError: If lengths differ, fewer than 2 elements, or either has zero variance
    """
    # Input validation
    if not isinstance(x, (list, tuple)):
        raise ValueError("x must be a list or tuple")
    if not isinstance(y, (list, tuple)):
        raise ValueError("y must be a list or tuple")
    
    # Check lengths match
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    # Check minimum length
    if len(x) < 2:
        raise ValueError("x and y must have at least 2 elements")
    
    # Validate all elements are numeric
    try:
        x_vals = [float(val) for val in x]
        y_vals = [float(val) for val in y]
    except (TypeError, ValueError):
        raise ValueError("All elements in x and y must be numeric")
    
    n = len(x_vals)
    
    # Calculate means
    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n
    
    # Calculate deviations and products
    deviations_x = [val - mean_x for val in x_vals]
    deviations_y = [val - mean_y for val in y_vals]
    
    # Calculate covariance and standard deviations
    covariance = sum(dx * dy for dx, dy in zip(deviations_x, deviations_y)) / n
    
    variance_x = sum(dx ** 2 for dx in deviations_x) / n
    variance_y = sum(dy ** 2 for dy in deviations_y) / n
    
    # Check for zero variance
    if variance_x == 0 or variance_y == 0:
        raise ValueError("x and y must have non-zero variance")
    
    # Calculate standard deviations
    std_x = variance_x ** 0.5
    std_y = variance_y ** 0.5
    
    # Calculate Pearson correlation coefficient
    r = covariance / (std_x * std_y)
    
    # Round to 4 decimal places
    return round(r, 4)
