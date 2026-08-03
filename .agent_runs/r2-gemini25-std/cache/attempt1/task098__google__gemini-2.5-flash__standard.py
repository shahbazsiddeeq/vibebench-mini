import math

def pearson_r(x, y):
    """
    Calculates the Pearson correlation coefficient between two lists.

    Args:
        x (list): The first list of numerical data.
        y (list): The second list of numerical data.

    Returns:
        float: The Pearson correlation coefficient, rounded to 4 decimal places.

    Raises:
        ValueError: If the lengths of x and y differ, if either list has fewer
                    than 2 elements, or if either list has zero variance.
    """
    n = len(x)

    if n != len(y):
        raise ValueError("Input lists must have the same length.")
    if n < 2:
        raise ValueError("Input lists must contain at least 2 elements.")

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    # Calculate deviations from the mean
    dev_x = [xi - mean_x for xi in x]
    dev_y = [yi - mean_y for yi in y]

    # Calculate sum of products of deviations
    sum_prod_dev = sum(dx * dy for dx, dy in zip(dev_x, dev_y))

    # Calculate sum of squared deviations
    sum_sq_dev_x = sum(dx**2 for dx in dev_x)
    sum_sq_dev_y = sum(dy**2 for dy in dev_y)

    # Check for zero variance
    if sum_sq_dev_x == 0 or sum_sq_dev_y == 0:
        raise ValueError("Cannot compute Pearson correlation for a list with zero variance.")

    # Calculate the denominator
    denominator = math.sqrt(sum_sq_dev_x * sum_sq_dev_y)

    # Calculate Pearson correlation coefficient
    r = sum_prod_dev / denominator

    return round(r, 4)
