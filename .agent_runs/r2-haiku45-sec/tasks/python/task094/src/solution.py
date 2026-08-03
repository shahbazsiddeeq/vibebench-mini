import statistics
from typing import Union


def describe(data):
    """
    Calculate descriptive statistics for a dataset.
    
    Args:
        data: A list or sequence of numeric values
        
    Returns:
        A dictionary with keys: count, mean, median, mode, std_dev, min, max, range
        All numeric values except count are rounded to 4 decimal places.
        
    Raises:
        ValueError: If data is empty
    """
    # Validate input
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Convert to list to allow multiple iterations
    data_list = list(data)
    
    # Validate that all elements are numeric
    try:
        numeric_data = [float(x) for x in data_list]
    except (TypeError, ValueError):
        raise ValueError("All elements must be numeric")
    
    count = len(numeric_data)
    
    # Calculate mean
    mean = sum(numeric_data) / count
    mean_rounded = round(mean, 4)
    
    # Calculate median
    sorted_data = sorted(numeric_data)
    if count % 2 == 1:
        median = sorted_data[count // 2]
    else:
        median = (sorted_data[count // 2 - 1] + sorted_data[count // 2]) / 2
    median_rounded = round(median, 4)
    
    # Calculate mode
    mode = None
    if count > 1:
        # Count frequencies
        freq_dict = {}
        for value in numeric_data:
            freq_dict[value] = freq_dict.get(value, 0) + 1
        
        # Find maximum frequency
        max_freq = max(freq_dict.values())
        
        # If max frequency is greater than 1, there's a mode
        if max_freq > 1:
            # Get all values with max frequency and pick the smallest
            mode_candidates = [v for v, f in freq_dict.items() if f == max_freq]
            mode = min(mode_candidates)
    
    # Calculate population standard deviation (ddof=0)
    if count == 1:
        std_dev = 0.0
    else:
        variance = sum((x - mean) ** 2 for x in numeric_data) / count
        std_dev = variance ** 0.5
    std_dev_rounded = round(std_dev, 4)
    
    # Calculate min and max
    min_val = min(numeric_data)
    max_val = max(numeric_data)
    
    # Calculate range
    range_val = max_val - min_val
    
    return {
        "count": count,
        "mean": mean_rounded,
        "median": median_rounded,
        "mode": mode,
        "std_dev": std_dev_rounded,
        "min": min_val,
        "max": max_val,
        "range": range_val
    }
