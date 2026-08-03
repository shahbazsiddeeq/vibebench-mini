def linear_regression(xs, ys):
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    n = len(xs)
    if n < 2:
        raise ValueError("at least 2 points are required")

    mx = sum(xs) / n
    my = sum(ys) / n

    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)

    if den == 0:
        raise ValueError("all x values are identical; slope is undefined")

    slope = num / den
    intercept = my - slope * mx

    return (round(slope, 6), round(intercept, 6))
