# src/solution.py

from typing import List
import math

def pearson_r(x: List[float], y: List[float]) -> float:
    # Validate input lengths
    if len(x) != len(y):
        raise ValueError("Input lists must have the same length.")
    
    n = len(x)
    
    # Validate minimum length
    if n < 2:
        raise ValueError("Input lists must contain at least two elements.")
    
    # Calculate means
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    # Calculate covariance and variances
    covariance = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    variance_x = sum((xi - mean_x) ** 2 for xi in x)
    variance_y = sum((yi - mean_y) ** 2 for yi in y)
    
    # Validate variances
    if variance_x == 0 or variance_y == 0:
        raise ValueError("Input lists must not have zero variance.")
    
    # Calculate Pearson correlation coefficient
    r = covariance / math.sqrt(variance_x * variance_y)
    
    return round(r, 4)
