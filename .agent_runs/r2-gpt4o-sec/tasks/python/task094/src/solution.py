import math
from collections import Counter
from typing import List, Dict, Union

def describe(data: List[Union[int, float]]) -> Dict[str, Union[int, float, None]]:
    if not data:
        raise ValueError("Data list cannot be empty.")
    
    n = len(data)
    sorted_data = sorted(data)
    
    # Count
    count = n
    
    # Mean
    mean = sum(data) / n
    
    # Median
    if n % 2 == 1:
        median = sorted_data[n // 2]
    else:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    
    # Mode
    frequency = Counter(data)
    max_freq = max(frequency.values())
    mode_candidates = [k for k, v in frequency.items() if v == max_freq]
    mode = min(mode_candidates) if max_freq > 1 else None
    
    # Standard Deviation
    if n == 1:
        std_dev = 0.0
    else:
        mean_diff_squared = [(x - mean) ** 2 for x in data]
        variance = sum(mean_diff_squared) / n
        std_dev = math.sqrt(variance)
    
    # Min and Max
    min_value = sorted_data[0]
    max_value = sorted_data[-1]
    
    # Range
    range_value = max_value - min_value
    
    return {
        "count": count,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "mode": mode,
        "std_dev": round(std_dev, 4),
        "min": min_value,
        "max": max_value,
        "range": range_value
    }
