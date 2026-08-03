import math

def percentile(data, p):
    """
    Calculates the p-th percentile of a list of numerical data using linear interpolation.

    Args:
        data (list): A list of numerical values.
        p (float or int): The percentile to calculate, a value between 0 and 100 (inclusive).

    Returns:
        float: The calculated p-th percentile.

    Raises:
        ValueError: If data is empty, or if p is not within the range [0, 100].
        TypeError: If data contains non-numeric types or if p is not a number.
    """
    if not isinstance(data, list):
        raise TypeError("Input 'data' must be a list.")
    if not all(isinstance(x, (int, float)) for x in data):
        raise TypeError("All elements in 'data' must be numbers.")
    if not isinstance(p, (int, float)):
        raise TypeError("Input 'p' must be a number.")

    if not data:
        raise ValueError("Input 'data' cannot be empty.")
    if not (0 <= p <= 100):
        raise ValueError("Percentile 'p' must be between 0 and 100, inclusive.")

    n = len(data)
    sorted_data = sorted(data)

    if p == 0:
        return float(sorted_data[0])
    if p == 100:
        return float(sorted_data[n - 1])

    # Calculate the rank (index)
    # The formula for rank (L) is (n - 1) * p / 100
    # This is consistent with the linear interpolation method where the 0th element
    # corresponds to the 0th percentile and the (n-1)th element corresponds to the 100th percentile.
    rank = (n - 1) * p / 100.0

    # Separate the integer and fractional parts of the rank
    k = math.floor(rank)
    f = rank - k

    # If k is the last index, or if f is 0, the percentile is the value at index k
    if k == n - 1 or f == 0:
        return float(sorted_data[int(k)])
    else:
        # Linear interpolation
        # P_p = X_k + f * (X_{k+1} - X_k)
        return float(sorted_data[int(k)]) + f * (float(sorted_data[int(k + 1)]) - float(sorted_data[int(k)]))
