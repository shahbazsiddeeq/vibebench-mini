def min_max_normalize(values, new_min=0.0, new_max=1.0):
    if not values:
        raise ValueError("values must not be empty")

    lo = min(values)
    hi = max(values)

    if hi == lo:
        return [round(float(new_min), 6) for _ in values]

    span = hi - lo
    new_span = new_max - new_min

    result = []
    for x in values:
        scaled = new_min + (x - lo) / span * new_span
        result.append(round(float(scaled), 6))
    return result
