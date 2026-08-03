def weighted_average(values, weights):
    """Return sum(v*w)/sum(w) rounded to 6 decimals as a float.

    Raises ValueError on empty inputs, length mismatch, or zero total weight.
    """
    if not values or not weights:
        raise ValueError("values and weights must be non-empty")
    if len(values) != len(weights):
        raise ValueError("values and weights must have equal length")

    total_weight = 0.0
    weighted_sum = 0.0
    for v, w in zip(values, weights):
        weighted_sum += v * w
        total_weight += w

    if total_weight == 0:
        raise ValueError("sum of weights must not be zero")

    return round(weighted_sum / total_weight, 6)
