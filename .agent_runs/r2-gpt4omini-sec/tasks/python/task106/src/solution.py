# src/solution.py

from typing import List, Tuple
import numbers

def histogram(data: List[float], bins: int) -> List[Tuple[float, float, int]]:
    if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Data must be a list of numbers.")
    if not isinstance(bins, int) or bins < 1:
        raise ValueError("Number of bins must be an integer greater than 0.")
    if not data:
        raise ValueError("Data cannot be empty.")
    
    min_val = min(data)
    max_val = max(data)

    if min_val == max_val:
        return [(min_val, max_val, len(data))]

    bin_width = (max_val - min_val) / bins
    histogram_bins = []

    for i in range(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        count = sum(1 for x in data if bin_start <= x < bin_end) if i < bins - 1 else sum(1 for x in data if bin_start <= x <= max_val)
        histogram_bins.append((bin_start, bin_end, count))

    return histogram_bins
