def weighted_average(values, weights):
    if not values or not weights:
        raise ValueError("values and weights must be non-empty")
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("sum of weights must not be zero")
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    return round(float(weighted_sum) / total_weight, 6)
