import math

def z_scores(data):
    """
    Calculates the z-scores for a list of numerical data.

    Args:
        data (list): A list of numbers.

    Returns:
        list: A list of z-scores, where each z-score is (x - mean) / std.

    Raises:
        ValueError: If the length of data is less than 2 or if the
                    population standard deviation is zero.
        TypeError: If data is not a list or contains non-numeric elements.
    """
    if not isinstance(data, list):
        raise TypeError("Input 'data' must be a list.")

    if len(data) < 2:
        raise ValueError("Input 'data' must contain at least two elements.")

    # Validate that all elements are numbers
    for item in data:
        if not isinstance(item, (int, float)):
            raise TypeError("All elements in 'data' must be numbers.")

    n = len(data)
    
    # Calculate the mean
    try:
        mean = sum(data) / n
    except ZeroDivisionError: # Should not happen due to len(data) < 2 check, but good for robustness
        raise ValueError("Input 'data' must contain at least two elements.")

    # Calculate the population standard deviation (ddof=0)
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        raise ValueError("The standard deviation is zero. Cannot calculate z-scores.")

    # Calculate z-scores
    z_scores_list = [(x - mean) / std_dev for x in data]

    return z_scores_list
