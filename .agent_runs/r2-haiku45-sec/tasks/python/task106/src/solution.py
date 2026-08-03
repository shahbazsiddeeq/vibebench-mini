def histogram(data, bins):
    """
    Create a histogram with equal-width bins.
    
    Args:
        data: List of numeric values
        bins: Number of bins (must be >= 1)
    
    Returns:
        List of (bin_start, bin_end, count) tuples
    
    Raises:
        ValueError: If bins < 1 or data is empty
    """
    # Input validation
    if not isinstance(bins, int) or bins < 1:
        raise ValueError("bins must be an integer >= 1")
    
    if not data:
        raise ValueError("data cannot be empty")
    
    # Convert data to list of numbers for validation
    try:
        numeric_data = [float(x) for x in data]
    except (TypeError, ValueError):
        raise ValueError("all data values must be numeric")
    
    if not numeric_data:
        raise ValueError("data cannot be empty")
    
    min_val = min(numeric_data)
    max_val = max(numeric_data)
    
    # Special case: all values are equal
    if min_val == max_val:
        return [(float(min_val), float(max_val), len(numeric_data))]
    
    # Calculate bin width
    bin_width = (max_val - min_val) / bins
    
    # Initialize bin counts
    bin_counts = [0] * bins
    
    # Assign each data point to a bin
    for value in numeric_data:
        if value == max_val:
            # Max value goes to the last bin
            bin_counts[bins - 1] += 1
        else:
            # Calculate which bin this value belongs to
            bin_index = int((value - min_val) / bin_width)
            # Ensure bin_index is within valid range (handle floating point edge cases)
            bin_index = min(bin_index, bins - 1)
            bin_counts[bin_index] += 1
    
    # Create result tuples
    result = []
    for i in range(bins):
        bin_start = min_val + i * bin_width
        bin_end = min_val + (i + 1) * bin_width
        count = bin_counts[i]
        result.append((float(bin_start), float(bin_end), count))
    
    return result
