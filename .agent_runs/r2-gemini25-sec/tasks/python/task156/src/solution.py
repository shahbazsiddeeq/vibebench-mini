def weighted_average(values, weights):
    """
    Calculates the weighted arithmetic mean of a list of values.

    Args:
        values (list): A list of numbers (ints or floats).
        weights (list): A list of numbers (ints or floats) representing the weights.

    Returns:
        float: The weighted average, rounded to 6 decimal places.

    Raises:
        ValueError: If values is empty, weights is empty, lists have different lengths,
                    or the sum of weights is zero.
    """
    if not values:
        raise ValueError("The 'values' list cannot be empty.")
    if not weights:
        raise ValueError("The 'weights' list cannot be empty.")
    if len(values) != len(weights):
        raise ValueError("The 'values' and 'weights' lists must have the same length.")

    # Input validation: Ensure all elements are numbers (int or float)
    for val in values:
        if not isinstance(val, (int, float)):
            raise ValueError("All elements in 'values' must be numbers.")
    for weight in weights:
        if not isinstance(weight, (int, float)):
            raise ValueError("All elements in 'weights' must be numbers.")

    sum_products = 0.0
    sum_weights = 0.0

    for i in range(len(values)):
        sum_products += values[i] * weights[i]
        sum_weights += weights[i]

    if sum_weights == 0:
        raise ValueError("The sum of weights cannot be zero.")

    result = sum_products / sum_weights
    return round(result, 6)
