"""Utilities for min-max normalization."""


def min_max_normalize(values, new_min=0.0, new_max=1.0):
    """Return values scaled to the target range and rounded to six places."""
    if not values:
        raise ValueError("values must not be empty")

    lo = min(values)
    hi = max(values)

    if hi == lo:
        normalized = float(round(float(new_min), 6))
        return [normalized for _ in values]

    target_min = float(new_min)
    target_span = float(new_max) - target_min
    source_span = hi - lo

    return [
        float(round(target_min + (value - lo) / source_span * target_span, 6))
        for value in values
    ]
