# src/solution.py

def find_outliers(data, z_threshold=2.5):
    if len(data) < 2:
        raise ValueError("At least two data points are required.")
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = variance ** 0.5
    
    if std_dev == 0:
        return []
    
    outliers = []
    for x in data:
        z_score = (x - mean) / std_dev
        if abs(z_score) > z_threshold:
            outliers.append(x)
    
    return outliers
