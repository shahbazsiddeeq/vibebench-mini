# src/solution.py

import statistics

def find_outliers(data, z_threshold=2.5):
    if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Data must be a list of numbers.")
    
    if len(data) < 2:
        raise ValueError("At least two data points are required.")
    
    mean = statistics.mean(data)
    variance = statistics.variance(data, xbar=mean) if len(data) > 1 else 0
    std_dev = variance ** 0.5
    
    if std_dev == 0:
        return []
    
    outliers = []
    for value in data:
        z_score = (value - mean) / std_dev
        if abs(z_score) > z_threshold:
            outliers.append(value)
    
    return outliers
