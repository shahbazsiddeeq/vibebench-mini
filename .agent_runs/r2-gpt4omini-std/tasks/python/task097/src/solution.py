# src/solution.py

def z_scores(data):
    if len(data) < 2:
        raise ValueError("Data must contain at least two elements.")
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5
    
    if std_dev == 0:
        raise ValueError("Standard deviation cannot be zero.")
    
    return [(x - mean) / std_dev for x in data]
