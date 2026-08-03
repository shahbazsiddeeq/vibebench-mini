def percentile(data, p):
    """
    Calculates the p-th percentile of a list of numerical data using linear interpolation.

    Args:
        data (list): A list of numerical values.
        p (int or float): The percentile to calculate, a value between 0 and 100 (inclusive).

    Returns:
        float: The calculated p-th percentile.

    Raises:
        ValueError: If data is empty or if p is outside the range [0, 100].
    """
    if not data:
        raise ValueError("Input data cannot be empty.")
    if not (0 <= p <= 100):
        raise ValueError("Percentile 'p' must be between 0 and 100 (inclusive).")

    sorted_data = sorted(data)
    n = len(sorted_data)

    if p == 0:
        return float(sorted_data[0])
    if p == 100:
        return float(sorted_data[-1])

    # Calculate the rank (index)
    # The formula for rank is (p / 100) * (n - 1) + 1
    # However, for 0-based indexing, it's (p / 100) * (n - 1)
    # Let's use the common definition where the rank is (p/100) * (N-1)
    # and then interpolate between the two closest data points.
    # The index in a 0-based array would be (p/100) * (N-1)
    
    # Convert p to a fraction
    fractional_rank = (p / 100.0) * (n - 1)

    # Get the integer and fractional parts of the rank
    lower_index = int(fractional_rank)
    fraction = fractional_rank - lower_index

    if fraction == 0:
        # If the rank is an integer, the percentile is the value at that index
        return float(sorted_data[lower_index])
    else:
        # If the rank is not an integer, interpolate between the two closest values
        # The value at lower_index and lower_index + 1
        v1 = sorted_data[lower_index]
        v2 = sorted_data[lower_index + 1]
        return v1 + fraction * (v2 - v1)
