# src/solution.py

def histogram(data, bins):
    if bins < 1:
        raise ValueError("Number of bins must be at least 1.")
    if not data:
        raise ValueError("Data cannot be empty.")
    
    min_val = min(data)
    max_val = max(data)
    
    if min_val == max_val:
        return [(min_val, max_val, len(data))]
    
    bin_width = (max_val - min_val) / bins
    result = []
    
    for i in range(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        count = sum(1 for x in data if bin_start <= x < bin_end) if i < bins - 1 else sum(1 for x in data if bin_start <= x <= max_val)
        result.append((bin_start, bin_end, count))
    
    return result
