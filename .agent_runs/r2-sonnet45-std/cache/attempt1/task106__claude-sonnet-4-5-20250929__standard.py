def histogram(data, bins):
    """
    Returns a list of (bin_start, bin_end, count) tuples with equal-width bins.
    
    Args:
        data: List of numeric values
        bins: Number of bins (must be >= 1)
    
    Returns:
        List of (bin_start, bin_end, count) tuples
        
    Raises:
        ValueError: If bins < 1 or data is empty
    """
    # Validate inputs
    if bins < 1:
        raise ValueError("bins must be at least 1")
    
    if not data:
        raise ValueError("data cannot be empty")
    
    # Handle case where all values are equal
    min_val = min(data)
    max_val = max(data)
    
    if min_val == max_val:
        return [(float(min_val), float(max_val), len(data))]
    
    # Calculate bin width
    bin_width = (max_val - min_val) / bins
    
    # Initialize bins
    result = []
    
    # Create bins and count values
    for i in range(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        
        # Count values in this bin
        count = 0
        for value in data:
            if i == bins - 1:  # Last bin is closed [start, end]
                if bin_start <= value <= bin_end:
                    count += 1
            else:  # Other bins are half-open [start, end)
                if bin_start <= value < bin_end:
                    count += 1
        
        result.append((float(bin_start), float(bin_end), count))
    
    return result
