def freq_dist(data):
    """
    Calculates the frequency distribution of elements in a list.

    Args:
        data: A list of hashable elements.

    Returns:
        A dictionary where keys are the unique elements from the input list
        and values are their relative frequencies, rounded to 4 decimal places.

    Raises:
        ValueError: If the input data list is empty.
        TypeError: If data is not a list or contains unhashable elements.
    """
    if not isinstance(data, list):
        raise TypeError("Input 'data' must be a list.")

    if not data:
        raise ValueError("Input 'data' cannot be empty.")

    total_elements = len(data)
    counts = {}

    for item in data:
        # Attempt to hash the item to ensure it's a valid dictionary key.
        # This implicitly handles unhashable types by raising a TypeError.
        try:
            hash(item)
        except TypeError as e:
            raise TypeError(f"Elements in 'data' must be hashable. Encountered unhashable type: {type(item).__name__}") from e
        
        counts[item] = counts.get(item, 0) + 1

    frequency_distribution = {}
    for item, count in counts.items():
        relative_frequency = count / total_elements
        frequency_distribution[item] = round(relative_frequency, 4)

    return frequency_distribution
