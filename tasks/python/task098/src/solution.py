import math


def pearson_r(x: list[float], y: list[float]) -> float:
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    if n < 2:
        raise ValueError("Need at least 2 data points")
    mx = sum(x) / n
    my = sum(y) / n
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    if den == 0:
        raise ValueError("Standard deviation is zero for one of the inputs")
    return round(num / den, 4)
