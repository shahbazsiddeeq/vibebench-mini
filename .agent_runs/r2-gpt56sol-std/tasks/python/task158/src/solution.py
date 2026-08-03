"""Simple ordinary least-squares linear regression."""

from typing import Sequence, Tuple


def linear_regression(
    xs: Sequence[float], ys: Sequence[float]
) -> Tuple[float, float]:
    """Fit and return the OLS line as ``(slope, intercept)``."""
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")

    n = len(xs)
    if n < 2:
        raise ValueError("at least two points are required")

    mx = sum(xs) / n
    my = sum(ys) / n

    numerator = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denominator = sum((x - mx) ** 2 for x in xs)

    if denominator == 0:
        raise ValueError("slope is undefined when all x values are identical")

    slope = numerator / denominator
    intercept = my - slope * mx

    return float(round(slope, 6)), float(round(intercept, 6))
