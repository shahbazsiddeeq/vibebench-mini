from collections import Counter


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
    """
    if not data:
        raise ValueError("Input data cannot be empty.")

    total_elements = len(data)
    counts = Counter(data)
    
    frequency_distribution = {}
    for item, count in counts.items():
        relative_frequency = count / total_elements
        frequency_distribution[item] = round(relative_frequency, 4)
        
    return frequency_distribution
