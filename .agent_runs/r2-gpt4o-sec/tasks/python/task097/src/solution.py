import math

def z_scores(data):
    if not isinstance(data, list) or len(data) < 2:
        raise ValueError("Data must be a list with at least two elements.")
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = math.sqrt(variance)
    
    if std_dev == 0:
        raise ValueError("Standard deviation cannot be zero.")
    
    return [(x - mean) / std_dev for x in data]
