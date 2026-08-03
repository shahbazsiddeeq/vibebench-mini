def linear_regression(xs, ys):
    """Fit y = slope*x + intercept by ordinary least squares.

    Returns (slope, intercept), each rounded to 6 decimals.
    Raises ValueError on length mismatch, fewer than 2 points, or constant x.
    """
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have equal length")
    n = len(xs)
    if n < 2:
        raise ValueError("need at least 2 points")

    mx = sum(xs) / n
    my = sum(ys) / n

    numerator = 0.0
    denominator = 0.0
    for x, y in zip(xs, ys):
        dx = x - mx
        numerator += dx * (y - my)
        denominator += dx * dx

    if denominator == 0:
        raise ValueError("x values are constant; slope is undefined")

    slope = numerator / denominator
    intercept = my - slope * mx
    return (round(slope, 6), round(intercept, 6))
