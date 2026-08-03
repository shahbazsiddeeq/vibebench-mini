def histogram(data, bins):
    if bins < 1 or not data:
        raise ValueError("Number of bins must be at least 1 and data must not be empty.")
    
    min_val = min(data)
    max_val = max(data)
    
    if min_val == max_val:
        return [(min_val, max_val, len(data))]
    
    bin_width = (max_val - min_val) / bins
    result = []
    
    for i in range(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        if i == bins - 1:
            bin_end = max_val
        
        count = sum(bin_start <= x < bin_end for x in data)
        if i == bins - 1:
            count += sum(x == max_val for x in data)
        
        result.append((bin_start, bin_end, count))
    
    return result
