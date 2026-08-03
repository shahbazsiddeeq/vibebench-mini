def linear_regression(xs, ys):
    """
    Fits a simple ordinary-least-squares line y = slope * x + intercept
    to the paired data in lists `xs` and `ys`.

    Args:
        xs (list): A list of x-coordinates.
        ys (list): A list of y-coordinates.

    Returns:
        tuple: A tuple (slope, intercept) where each value is a float
               rounded to 6 decimal places.

    Raises:
        ValueError: If `xs` and `ys` have different lengths, or if there are
                    fewer than 2 points, or if all x values are identical.
    """
    if len(xs) != len(ys):
        raise ValueError("Input lists xs and ys must have the same length.")
    if len(xs) < 2:
        raise ValueError("At least 2 points are required for linear regression.")

    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n

    sum_of_products = 0.0
    sum_of_squares = 0.0

    for x, y in zip(xs, ys):
        sum_of_products += (x - mx) * (y - my)
        sum_of_squares += (x - mx) ** 2

    if sum_of_squares == 0:
        raise ValueError("All x values are identical, resulting in an undefined slope.")

    slope = sum_of_products / sum_of_squares
    intercept = my - slope * mx

    return round(slope, 6), round(intercept, 6)
