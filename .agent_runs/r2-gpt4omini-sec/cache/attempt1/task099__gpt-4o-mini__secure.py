# src/solution.py

from typing import List
import statistics

def find_outliers(data: List[float], z_threshold: float = 2.5) -> List[float]:
    if len(data) < 2:
        raise ValueError("At least two data points are required.")
    
    mean = statistics.mean(data)
    variance = statistics.variance(data, xbar=mean) * (len(data) / (len(data) - 1))  # Population variance
    std_dev = variance ** 0.5
    
    if std_dev == 0:
        return []
    
    outliers = []
    for value in data:
        z_score = (value - mean) / std_dev
        if abs(z_score) > z_threshold:
            outliers.append(value)
    
    return outliers
