def freq_dist(data):
    """
    Calculate the relative frequency distribution of values in data.
    
    Args:
        data: An iterable of hashable values
        
    Returns:
        A dictionary mapping each unique value to its relative frequency,
        rounded to 4 decimal places
        
    Raises:
        ValueError: If data is empty
    """
    # Validate input - convert to list to check length and iterate
    if not isinstance(data, (list, tuple, str)):
        try:
            data = list(data)
        except (TypeError, ValueError):
            raise ValueError("data must be iterable")
    
    # Check for empty data
    if len(data) == 0:
        raise ValueError("data cannot be empty")
    
    # Count occurrences of each value
    counts = {}
    for value in data:
        # Ensure value is hashable
        try:
            if value in counts:
                counts[value] += 1
            else:
                counts[value] = 1
        except TypeError:
            raise ValueError("all values in data must be hashable")
    
    # Calculate relative frequencies
    total = len(data)
    result = {}
    for value, count in counts.items():
        relative_freq = count / total
        # Round to 4 decimal places
        result[value] = round(relative_freq, 4)
    
    return result
