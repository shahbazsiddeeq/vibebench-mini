import math

def find_outliers(data, z_threshold=2.5):
    """
    Finds outliers in a list of numerical data using the z-score method.

    An outlier is defined as a data point whose absolute z-score is strictly
    greater than the given z_threshold. The z-score is calculated using the
    population standard deviation.

    Args:
        data (list): A list of numerical values.
        z_threshold (float): The threshold for the absolute z-score to
                             consider a point an outlier. Defaults to 2.5.

    Returns:
        list: A list of outlier values, in their original order.

    Raises:
        ValueError: If the input 'data' contains fewer than 2 elements.
    """
    n = len(data)

    if n < 2:
        raise ValueError("Input 'data' must contain at least 2 elements to calculate outliers.")

    mean = sum(data) / n

    # Calculate population variance
    # variance = sum((x - mean)**2 for x in data) / n
    # Using math.fsum for potentially better precision with floating point sums
    variance = math.fsum((x - mean)**2 for x in data) / n

    # Calculate population standard deviation
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        # If standard deviation is 0, all data points are identical.
        # No outliers can exist in this case.
        return []

    outliers = []
    for x in data:
        z_score = (x - mean) / std_dev
        if abs(z_score) > z_threshold:
            outliers.append(x)

    return outliers
