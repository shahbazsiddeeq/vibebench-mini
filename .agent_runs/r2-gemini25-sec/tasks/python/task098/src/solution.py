import math

def pearson_r(x, y):
    """
    Calculates the Pearson correlation coefficient between two lists.

    Args:
        x (list): A list of numerical data.
        y (list): A list of numerical data.

    Returns:
        float: The Pearson correlation coefficient, rounded to 4 decimal places.

    Raises:
        ValueError: If the lengths of x and y differ, if either list has fewer
                    than 2 elements, or if either list has zero variance.
    """
    if not isinstance(x, list) or not isinstance(y, list):
        raise ValueError("Inputs must be lists.")

    if len(x) != len(y):
        raise ValueError("Input lists must have the same length.")

    n = len(x)
    if n < 2:
        raise ValueError("Input lists must contain at least 2 elements.")

    # Input validation: Ensure all elements are numbers
    try:
        x_float = [float(val) for val in x]
        y_float = [float(val) for val in y]
    except (TypeError, ValueError) as e:
        raise ValueError(f"All elements in input lists must be numbers: {e}")

    sum_x = sum(x_float)
    sum_y = sum(y_float)
    sum_xy = sum(xi * yi for xi, yi in zip(x_float, y_float))
    sum_x2 = sum(xi * xi for xi in x_float)
    sum_y2 = sum(yi * yi for yi in y_float)

    try:
        numerator = n * sum_xy - sum_x * sum_y
        denominator_x = math.sqrt(n * sum_x2 - sum_x * sum_x)
        denominator_y = math.sqrt(n * sum_y2 - sum_y * sum_y)
    except OverflowError:
        # Handle cases where intermediate sums might be too large for float
        raise ValueError("Numerical overflow occurred during calculation. Input values might be too large.")

    if denominator_x == 0 or denominator_y == 0:
        raise ValueError("Cannot compute Pearson correlation: one or both inputs have zero variance.")

    try:
        correlation = numerator / (denominator_x * denominator_y)
    except ZeroDivisionError:
        # This case should ideally be caught by the denominator_x/y == 0 check,
        # but as a safeguard against floating point inaccuracies.
        raise ValueError("Cannot compute Pearson correlation: denominator is zero.")
    except OverflowError:
        raise ValueError("Numerical overflow occurred during final division.")

    # Ensure the result is within [-1, 1] due to potential floating point inaccuracies
    correlation = max(-1.0, min(1.0, correlation))

    return round(correlation, 4)
