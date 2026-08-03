# src/solution.py

import statistics

def z_scores(data):
    # Validate input
    if not isinstance(data, list):
        raise ValueError("Input must be a list.")
    
    if len(data) < 2:
        raise ValueError("At least two data points are required.")
    
    # Ensure all elements are numeric
    if not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("All elements in the data list must be numeric.")
    
    # Calculate mean and standard deviation
    mean = statistics.mean(data)
    std_dev = statistics.pstdev(data)  # Population standard deviation (ddof=0)
    
    if std_dev == 0:
        raise ValueError("Standard deviation cannot be zero.")
    
    # Calculate z-scores
    z_scores_list = [(x - mean) / std_dev for x in data]
    
    return z_scores_list
