"""Pearson Correlation Coefficient module."""


def pearson_r(x, y):
    """Compute Pearson correlation coefficient rounded to 4 decimal places.

    Raises ValueError if:
    - lengths differ
    - fewer than 2 elements
    - either x or y has zero variance
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    if n < 2:
        raise ValueError("x and y must have at least 2 elements")

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    sum_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    sum_x2 = sum((xi - mean_x) ** 2 for xi in x)
    sum_y2 = sum((yi - mean_y) ** 2 for yi in y)

    if sum_x2 == 0 or sum_y2 == 0:
        raise ValueError("x and y must have non-zero variance")

    r = sum_xy / (sum_x2 ** 0.5 * sum_y2 ** 0.5)
    return round(r, 4)
