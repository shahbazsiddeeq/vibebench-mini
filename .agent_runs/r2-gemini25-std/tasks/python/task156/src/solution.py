def weighted_average(values, weights):
    """
    Calculates the weighted arithmetic mean of values using weights.

    Args:
        values (list): A list of numbers (ints or floats).
        weights (list): A list of numbers (ints or floats) representing the weights.

    Returns:
        float: The weighted average rounded to 6 decimal places.

    Raises:
        ValueError: If values is empty, weights is empty, lists have different lengths,
                    or the sum of weights is zero.
    """
    if not values:
        raise ValueError("values cannot be empty")
    if not weights:
        raise ValueError("weights cannot be empty")
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")

    sum_of_products = sum(v * w for v, w in zip(values, weights))
    sum_of_weights = sum(weights)

    if sum_of_weights == 0:
        raise ValueError("Sum of weights cannot be zero")

    result = sum_of_products / sum_of_weights
    return round(result, 6)
