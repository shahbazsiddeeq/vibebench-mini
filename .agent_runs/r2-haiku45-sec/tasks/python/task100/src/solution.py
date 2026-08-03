def freq_dist(data):
    """
    Calculate the frequency distribution of data.
    
    Args:
        data: A sequence of values
        
    Returns:
        A dictionary mapping each unique value to its relative frequency
        (count / total length), rounded to 4 decimal places
        
    Raises:
        ValueError: If data is empty
    """
    # Validate input
    if not data:
        raise ValueError("data cannot be empty")
    
    # Ensure data is a sequence we can work with
    try:
        data_list = list(data)
    except TypeError:
        raise ValueError("data must be iterable")
    
    if len(data_list) == 0:
        raise ValueError("data cannot be empty")
    
    # Count occurrences of each value
    counts = {}
    for value in data_list:
        counts[value] = counts.get(value, 0) + 1
    
    # Calculate relative frequencies rounded to 4 decimal places
    total = len(data_list)
    result = {}
    for value, count in counts.items():
        relative_freq = round(count / total, 4)
        result[value] = relative_freq
    
    return result
