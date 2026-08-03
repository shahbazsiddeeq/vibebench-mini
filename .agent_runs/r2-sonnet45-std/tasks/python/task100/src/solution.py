def freq_dist(data):
    """
    Calculate the frequency distribution of values in data.
    
    Args:
        data: An iterable of values
        
    Returns:
        A dictionary mapping each unique value to its relative frequency,
        rounded to 4 decimal places
        
    Raises:
        ValueError: If data is empty
    """
    # Convert to list if needed to get length
    data_list = list(data)
    
    if not data_list:
        raise ValueError("Data cannot be empty")
    
    total = len(data_list)
    
    # Count occurrences
    counts = {}
    for value in data_list:
        counts[value] = counts.get(value, 0) + 1
    
    # Calculate relative frequencies
    result = {}
    for value, count in counts.items():
        relative_freq = count / total
        result[value] = round(relative_freq, 4)
    
    return result
