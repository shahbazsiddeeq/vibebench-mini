import math
from collections import Counter

def describe(data):
    if not data:
        raise ValueError("Input data cannot be empty.")

    count = len(data)
    data_sorted = sorted(data)
    
    # Mean
    mean = sum(data) / count

    # Median
    if count % 2 == 1:
        median = data_sorted[count // 2]
    else:
        mid1 = data_sorted[count // 2 - 1]
        mid2 = data_sorted[count // 2]
        median = (mid1 + mid2) / 2

    # Mode
    counts = Counter(data)
    max_freq = 0
    mode = None
    
    # Find the maximum frequency
    if counts:
        max_freq = max(counts.values())

    # Check if all values are unique
    if max_freq == 1 and count > 1:
        mode = None
    else:
        # Find all values with max_freq and pick the smallest one
        modes_candidates = [k for k, v in counts.items() if v == max_freq]
        if modes_candidates:
            mode = min(modes_candidates)
        else:
            mode = None # Should not happen if counts is not empty and max_freq > 0

    # Standard Deviation (population)
    if count <= 1:
        std_dev = 0.0
    else:
        variance = sum((x - mean) ** 2 for x in data) / count
        std_dev = math.sqrt(variance)

    # Min, Max, Range
    min_val = data_sorted[0]
    max_val = data_sorted[-1]
    data_range = max_val - min_val

    # Round numeric values to 4 decimal places
    mean = round(mean, 4)
    median = round(median, 4)
    std_dev = round(std_dev, 4)
    # min_val, max_val, data_range are integers or floats that don't need rounding unless they were results of calculations.
    # For the given problem, they are direct values or simple differences, so direct rounding might not be necessary
    # unless they are floats from the input. The example implies they are exact.
    # Let's ensure consistency for all numeric outputs that are not integers.
    min_val = round(min_val, 4) if isinstance(min_val, float) else min_val
    max_val = round(max_val, 4) if isinstance(max_val, float) else max_val
    data_range = round(data_range, 4) if isinstance(data_range, float) else data_range


    return {
        "count": count,
        "mean": mean,
        "median": median,
        "mode": mode,
        "std_dev": std_dev,
        "min": min_val,
        "max": max_val,
        "range": data_range,
    }
