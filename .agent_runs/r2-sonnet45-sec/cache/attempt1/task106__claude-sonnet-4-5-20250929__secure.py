def histogram(data, bins):
    """
    Create a histogram with equal-width bins.
    
    Args:
        data: Iterable of numeric values
        bins: Number of bins (must be >= 1)
    
    Returns:
        List of (bin_start, bin_end, count) tuples
    
    Raises:
        ValueError: If bins < 1 or data is empty
    """
    # Validate bins parameter
    if not isinstance(bins, int) or bins < 1:
        raise ValueError("bins must be an integer >= 1")
    
    # Convert data to list and validate
    data_list = list(data)
    if not data_list:
        raise ValueError("data cannot be empty")
    
    # Validate all data elements are numeric
    try:
        data_values = [float(x) for x in data_list]
    except (TypeError, ValueError):
        raise ValueError("all data elements must be numeric")
    
    # Find min and max
    min_val = min(data_values)
    max_val = max(data_values)
    
    # Special case: all values are equal
    if min_val == max_val:
        return [(float(min_val), float(max_val), len(data_values))]
    
    # Calculate bin width
    range_width = max_val - min_val
    bin_width = range_width / bins
    
    # Initialize bins
    bin_edges = []
    for i in range(bins):
        start = min_val + i * bin_width
        end = min_val + (i + 1) * bin_width
        bin_edges.append((float(start), float(end), 0))
    
    # Count values in each bin
    counts = [0] * bins
    
    for value in data_values:
        # Determine which bin this value belongs to
        if value == max_val:
            # Max value goes in the last bin (which is closed)
            counts[-1] += 1
        else:
            # Calculate bin index for values < max
            bin_index = int((value - min_val) / bin_width)
            # Clamp to valid range (shouldn't be needed but for safety)
            bin_index = max(0, min(bins - 1, bin_index))
            counts[bin_index] += 1
    
    # Build result with counts
    result = []
    for i in range(bins):
        start, end, _ = bin_edges[i]
        result.append((start, end, counts[i]))
    
    return result
