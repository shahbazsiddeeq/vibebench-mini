# src/solution.py

from typing import List, Dict, Union
from collections import Counter
import math

def describe(data: List[Union[int, float]]) -> Dict[str, Union[int, float, None]]:
    if not data:
        raise ValueError("Data list is empty")
    
    n = len(data)
    mean = sum(data) / n
    sorted_data = sorted(data)
    
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
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)
    
    # Min, Max, Range
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val
    
    return {
        "count": n,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "mode": mode,
        "std_dev": round(std_dev, 4),
        "min": min_val,
        "max": max_val,
        "range": range_val
    }
