def freq_dist(data):
    """
    Returns a dictionary of {value: relative_frequency} where each relative 
    frequency is the count of that value divided by len(data), rounded to 4 decimal places.
    
    Args:
        data: A list of values
        
    Returns:
        A dictionary mapping each unique value to its relative frequency
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("data cannot be empty")
    
    # Count occurrences of each value
    counts = {}
    for value in data:
        counts[value] = counts.get(value, 0) + 1
    
    # Calculate relative frequencies rounded to 4 decimal places
    total = len(data)
    result = {}
    for value, count in counts.items():
        result[value] = round(count / total, 4)
    
    return result
