def describe(data):
    """
    Calculate descriptive statistics for the given data.
    
    Args:
        data: A list or iterable of numeric values
        
    Returns:
        A dictionary containing count, mean, median, mode, std_dev, min, max, and range
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Convert to list if needed
    data_list = list(data)
    n = len(data_list)
    
    # Count
    count = n
    
    # Min and Max
    min_val = min(data_list)
    max_val = max(data_list)
    
    # Range
    range_val = max_val - min_val
    
    # Mean
    mean_val = sum(data_list) / n
    
    # Median
    sorted_data = sorted(data_list)
    if n % 2 == 0:
        median_val = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        median_val = sorted_data[n // 2]
    
    # Mode
    from collections import Counter
    freq_counter = Counter(data_list)
    max_freq = max(freq_counter.values())
    
    # If all values appear only once, mode is None
    if max_freq == 1:
        mode_val = None
    else:
        # Find all values with max frequency, then pick the smallest
        modes = [val for val, freq in freq_counter.items() if freq == max_freq]
        mode_val = min(modes)
    
    # Standard deviation (population)
    variance = sum((x - mean_val) ** 2 for x in data_list) / n
    std_dev_val = variance ** 0.5
    
    # Round numeric values to 4 decimal places (except count and mode)
    return {
        "count": count,
        "mean": round(mean_val, 4),
        "median": round(median_val, 4),
        "mode": mode_val,
        "std_dev": round(std_dev_val, 4),
        "min": min_val,
        "max": max_val,
        "range": range_val
    }
