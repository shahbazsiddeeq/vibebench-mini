# src/solution.py

import statistics
from collections import Counter

def describe(data):
    if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Input must be a list of numbers.")
    
    if len(data) == 0:
        raise ValueError("Data cannot be empty.")
    
    count = len(data)
    mean = round(statistics.mean(data), 4)
    median = round(statistics.median(data), 4)
    
    # Calculate mode
    frequency = Counter(data)
    max_freq = max(frequency.values())
    mode_candidates = [k for k, v in frequency.items() if v == max_freq]
    mode = min(mode_candidates) if max_freq > 1 else None
    
    std_dev = round(statistics.pstdev(data), 4) if count > 1 else 0.0
    min_value = min(data)
    max_value = max(data)
    range_value = max_value - min_value
    
    return {
        "count": count,
        "mean": mean,
        "median": median,
        "mode": mode,
        "std_dev": std_dev,
        "min": min_value,
        "max": max_value,
        "range": range_value
    }
