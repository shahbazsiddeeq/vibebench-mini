import math

def find_outliers(data, z_threshold=2.5):
    """
    Identifies outliers in a list of numerical data using the z-score method.

    An outlier is defined as a data point whose absolute z-score is strictly
    greater than the specified z_threshold. The z-score is calculated using
    the population standard deviation.

    Args:
        data (list): A list of numerical values (integers or floats).
        z_threshold (float): The threshold for the absolute z-score to
                             consider a data point an outlier. Must be
                             a non-negative float.

    Returns:
        list: A list of values identified as outliers, in their original order.

    Raises:
        ValueError: If the input 'data' contains fewer than 2 elements,
                    if 'data' contains non-numeric types, or if 'z_threshold'
                    is not a non-negative float.
    """
    if not isinstance(data, list):
        raise ValueError("Input 'data' must be a list.")
    if not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("All elements in 'data' must be numbers.")
    if len(data) < 2:
        raise ValueError("Input 'data' must contain at least 2 elements.")
    if not isinstance(z_threshold, (int, float)) or z_threshold < 0:
        raise ValueError("Input 'z_threshold' must be a non-negative number.")

    n = len(data)
    mean = sum(data) / n

    # Calculate population standard deviation
    # variance = sum((x - mean)^2) / N
    # std_dev = sqrt(variance)
    squared_deviations = [(x - mean) ** 2 for x in data]
    variance = sum(squared_deviations) / n
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        return []  # No deviation, so no outliers

    outliers = []
    for x in data:
        z_score = (x - mean) / std_dev
        if abs(z_score) > z_threshold:
            outliers.append(x)

    return outliers
