# src/solution.py

from collections import Counter
import statistics

def describe(data):
    if not data:
        raise ValueError("Data cannot be empty")

    count = len(data)
    mean = round(statistics.mean(data), 4)
    median = round(statistics.median(data), 4)
    
    # Calculate mode
    frequency = Counter(data)
    mode_data = frequency.most_common()
    max_freq = mode_data[0][1]
    modes = [num for num, freq in mode_data if freq == max_freq]
    mode = min(modes) if len(modes) > 1 else (modes[0] if max_freq > 1 else None)
    
    std_dev = round(statistics.pstdev(data), 4) if count > 1 else 0.0
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val

    return {
        "count": count,
        "mean": mean,
        "median": median,
        "mode": mode,
        "std_dev": std_dev,
        "min": min_val,
        "max": max_val,
        "range": range_val
    }
