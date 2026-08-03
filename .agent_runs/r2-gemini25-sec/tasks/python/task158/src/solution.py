def linear_regression(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """
    Fits a simple ordinary-least-squares line y = slope * x + intercept
    to the paired data in lists `xs` and `ys`.

    Args:
        xs: A list of x-coordinates (independent variable).
        ys: A list of y-coordinates (dependent variable).

    Returns:
        A tuple (slope, intercept) where each value is a float rounded to
        6 decimal places.

    Raises:
        ValueError: If `xs` and `ys` have different lengths, or if there are
                    fewer than 2 points, or if all x values are identical
                    (resulting in an undefined slope).
    """
    if not isinstance(xs, list) or not isinstance(ys, list):
        raise ValueError("Inputs 'xs' and 'ys' must be lists.")

    if len(xs) != len(ys):
        raise ValueError("Input lists 'xs' and 'ys' must have the same length.")

    n = len(xs)
    if n < 2:
        raise ValueError("At least 2 data points are required for linear regression.")

    # Validate that all elements are numbers (int or float)
    for i, x_val in enumerate(xs):
        if not isinstance(x_val, (int, float)):
            raise ValueError(f"Element at xs[{i}] is not a number: {x_val}")
    for i, y_val in enumerate(ys):
        if not isinstance(y_val, (int, float)):
            raise ValueError(f"Element at ys[{i}] is not a number: {y_val}")

    # Convert all inputs to floats to avoid type issues in calculations
    xs_float = [float(x) for x in xs]
    ys_float = [float(y) for y in ys]

    mx = sum(xs_float) / n
    my = sum(ys_float) / n

    sum_of_products = 0.0
    sum_of_squares_x = 0.0

    for x, y in zip(xs_float, ys_float):
        diff_x = x - mx
        diff_y = y - my
        sum_of_products += diff_x * diff_y
        sum_of_squares_x += diff_x * diff_x

    if sum_of_squares_x == 0:
        raise ValueError("All x-values are identical, resulting in an undefined slope.")

    slope = sum_of_products / sum_of_squares_x
    intercept = my - slope * mx

    return round(slope, 6), round(intercept, 6)
