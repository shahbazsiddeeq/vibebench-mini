def min_max_normalize(values, new_min=0.0, new_max=1.0):
    """Rescale values to [new_min, new_max] via min-max scaling.

    Returns a new list of floats rounded to 6 decimals. Constant series
    (hi == lo, including single element) maps every element to float(new_min).
    Empty input raises ValueError.
    """
    if not values:
        raise ValueError("values must be non-empty")

    lo = min(values)
    hi = max(values)

    if hi == lo:
        constant = round(float(new_min), 6)
        return [constant for _ in values]

    span = hi - lo
    target = new_max - new_min
    return [round(new_min + (x - lo) / span * target, 6) for x in values]
