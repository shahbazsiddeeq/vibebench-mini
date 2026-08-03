import statistics
from collections import Counter


def describe(data):
    """
    Returns a dict with descriptive statistics for the given data.
    
    Keys: count, mean, median, mode, std_dev, min, max, range
    All numeric values except count are rounded to 4 decimal places.
    std_dev is population standard deviation (ddof=0).
    mode is the most frequent value; if tie, use smallest; if all unique, use None.
    
    Raises ValueError for empty data.
    """
    if not data:
        raise ValueError("describe() requires non-empty data")
    
    data_list = list(data)
    n = len(data_list)
    
    # Count
    count = n
    
    # Mean
    mean = sum(data_list) / n
    mean = round(mean, 4)
    
    # Median
    sorted_data = sorted(data_list)
    if n % 2 == 1:
        median = sorted_data[n // 2]
    else:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    median = round(median, 4)
    
    # Mode
    counter = Counter(data_list)
    max_count = max(counter.values())
    
    if max_count == 1:
        # All values are unique
        mode = None
    else:
        # Get all values with max frequency, then pick the smallest
        mode_candidates = [val for val, count_val in counter.items() if count_val == max_count]
        mode = min(mode_candidates)
    
    # Standard deviation (population, ddof=0)
    if n == 1:
        std_dev = 0.0
    else:
        mean_val = sum(data_list) / n
        variance = sum((x - mean_val) ** 2 for x in data_list) / n
        std_dev = variance ** 0.5
    std_dev = round(std_dev, 4)
    
    # Min and Max
    min_val = min(data_list)
    max_val = max(data_list)
    
    # Range
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
