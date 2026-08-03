import math
from collections import Counter

def describe(data):
    """
    Calculates descriptive statistics for a list of numerical data.

    Args:
        data: A list of numbers (integers or floats).

    Returns:
        A dictionary containing the following statistics:
        - count: The number of elements in the data.
        - mean: The average of the data.
        - median: The middle value of the sorted data.
        - mode: The most frequent value. If multiple values tie, the smallest is chosen.
                If all values are unique, mode is None.
        - std_dev: The population standard deviation.
        - min: The minimum value in the data.
        - max: The maximum value in the data.
        - range: The difference between the maximum and minimum values.

    Raises:
        ValueError: If the input data list is empty.
        TypeError: If data contains non-numeric types.
    """
    if not data:
        raise ValueError("Input data cannot be empty.")

    # Input validation and type checking
    processed_data = []
    for item in data:
        if not isinstance(item, (int, float)):
            raise TypeError("All elements in data must be numbers.")
        processed_data.append(float(item))

    n = len(processed_data)
    
    # Count
    count = n

    # Min, Max, Range
    min_val = min(processed_data)
    max_val = max(processed_data)
    data_range = round(max_val - min_val, 4)

    # Mean
    data_sum = sum(processed_data)
    mean = round(data_sum / n, 4)

    # Median
    sorted_data = sorted(processed_data)
    if n % 2 == 1:
        median = round(sorted_data[n // 2], 4)
    else:
        mid1 = sorted_data[n // 2 - 1]
        mid2 = sorted_data[n // 2]
        median = round((mid1 + mid2) / 2, 4)

    # Mode
    counts = Counter(processed_data)
    if n == len(counts): # All values are unique
        mode = None
    else:
        max_freq = 0
        current_modes = []
        for value, freq in counts.items():
            if freq > max_freq:
                max_freq = freq
                current_modes = [value]
            elif freq == max_freq:
                current_modes.append(value)
        mode = min(current_modes) # Smallest value if tie

    # Population Standard Deviation
    if n == 1:
        std_dev = 0.0
    else:
        variance = sum((x - mean) ** 2 for x in processed_data) / n
        std_dev = round(math.sqrt(variance), 4)

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
