def weighted_average(values, weights):
    """Return the weighted arithmetic mean rounded to six decimal places."""
    if not values or not weights:
        raise ValueError("values and weights must be non-empty")
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")

    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("sum of weights must not be zero")

    result = sum(value * weight for value, weight in zip(values, weights))
    return float(round(result / total_weight, 6))
