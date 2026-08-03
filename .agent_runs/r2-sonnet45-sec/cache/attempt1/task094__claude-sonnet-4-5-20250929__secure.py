import math
from typing import List, Dict, Any, Union


def describe(data: List[Union[int, float]]) -> Dict[str, Any]:
    """
    Calculate descriptive statistics for a list of numeric data.
    
    Args:
        data: A list of numeric values (int or float)
        
    Returns:
        A dictionary containing:
        - count: number of elements
        - mean: arithmetic mean (rounded to 4 decimal places)
        - median: middle value (rounded to 4 decimal places)
        - mode: most frequent value (smallest if tie), None if all unique
        - std_dev: population standard deviation (rounded to 4 decimal places)
        - min: minimum value
        - max: maximum value
        - range: difference between max and min
        
    Raises:
        ValueError: if data is empty
    """
    # Validate input
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Validate that all elements are numeric
    for item in data:
        if not isinstance(item, (int, float)):
            raise ValueError("All data elements must be numeric")
    
    # Count
    count = len(data)
    
    # Min and Max
    min_val = min(data)
    max_val = max(data)
    
    # Range
    range_val = max_val - min_val
    
    # Mean
    mean_val = sum(data) / count
    
    # Median
    sorted_data = sorted(data)
    if count % 2 == 0:
        median_val = (sorted_data[count // 2 - 1] + sorted_data[count // 2]) / 2
    else:
        median_val = sorted_data[count // 2]
    
    # Mode
    # Count frequency of each value
    frequency = {}
    for value in data:
        frequency[value] = frequency.get(value, 0) + 1
    
    # Find maximum frequency
    max_frequency = max(frequency.values())
    
    # If all values appear only once, mode is None
    if max_frequency == 1:
        mode_val = None
    else:
        # Find all values with maximum frequency and pick the smallest
        modes = [value for value, freq in frequency.items() if freq == max_frequency]
        mode_val = min(modes)
    
    # Population standard deviation (ddof=0)
    if count == 1:
        std_dev_val = 0.0
    else:
        variance = sum((x - mean_val) ** 2 for x in data) / count
        std_dev_val = math.sqrt(variance)
    
    # Round numeric values to 4 decimal places
    mean_rounded = round(mean_val, 4)
    median_rounded = round(median_val, 4)
    std_dev_rounded = round(std_dev_val, 4)
    
    return {
        "count": count,
        "mean": mean_rounded,
        "median": median_rounded,
        "mode": mode_val,
        "std_dev": std_dev_rounded,
        "min": min_val,
        "max": max_val,
        "range": range_val
    }
