import math
from typing import List

def find_outliers(data: List[float], z_threshold: float = 2.5) -> List[float]:
    if len(data) < 2:
        raise ValueError("Data must contain at least two elements.")
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = math.sqrt(variance)
    
    if std_dev == 0:
        return []
    
    outliers = []
    for x in data:
        z_score = (x - mean) / std_dev
        if abs(z_score) > z_threshold:
            outliers.append(x)
    
    return outliers
