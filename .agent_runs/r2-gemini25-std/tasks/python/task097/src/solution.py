import math

def z_scores(data):
    """
    Calculates the z-scores for each element in a list of numerical data.

    Args:
        data (list): A list of numbers.

    Returns:
        list: A list of z-scores, where each z-score is (x - mean) / std.

    Raises:
        ValueError: If the length of data is less than 2 or if the standard
                    deviation is zero.
    """
    n = len(data)
    if n < 2:
        raise ValueError("Input data must contain at least two elements.")

    mean = sum(data) / n

    # Calculate population standard deviation (ddof=0)
    # Sum of squared differences from the mean
    sum_sq_diff = sum((x - mean) ** 2 for x in data)
    
    # Variance
    variance = sum_sq_diff / n
    
    # Standard deviation
    std_dev = math.sqrt(variance)

    if std_dev == 0:
        raise ValueError("Standard deviation is zero, cannot compute z-scores.")

    # Calculate z-scores
    z_score_list = [(x - mean) / std_dev for x in data]

    return z_score_list
