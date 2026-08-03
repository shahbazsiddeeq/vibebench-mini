def linear_regression(xs, ys):
    """
    Fit a simple ordinary-least-squares line y = slope * x + intercept.
    
    Args:
        xs: List of x values
        ys: List of y values
    
    Returns:
        Tuple of (slope, intercept) rounded to 6 decimal places
    
    Raises:
        ValueError: If xs and ys have different lengths, fewer than 2 points,
                   or all x values are identical
    """
    # Validate inputs are lists or sequences
    if not hasattr(xs, '__len__') or not hasattr(ys, '__len__'):
        raise ValueError("xs and ys must be sequences")
    
    # Check lengths match
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    
    # Check minimum number of points
    if len(xs) < 2:
        raise ValueError("At least 2 points are required")
    
    # Validate all elements are numeric
    try:
        xs_float = [float(x) for x in xs]
        ys_float = [float(y) for y in ys]
    except (TypeError, ValueError):
        raise ValueError("All elements in xs and ys must be numeric")
    
    # Calculate means
    n = len(xs_float)
    mx = sum(xs_float) / n
    my = sum(ys_float) / n
    
    # Calculate sum of products and sum of squares
    sum_products = sum((x - mx) * (y - my) for x, y in zip(xs_float, ys_float))
    sum_squares = sum((x - mx) ** 2 for x in xs_float)
    
    # Check for vertical line (all x values identical)
    if sum_squares == 0:
        raise ValueError("All x values are identical (undefined slope)")
    
    # Calculate slope and intercept
    slope = sum_products / sum_squares
    intercept = my - slope * mx
    
    # Round to 6 decimal places
    slope_rounded = round(slope, 6)
    intercept_rounded = round(intercept, 6)
    
    return (slope_rounded, intercept_rounded)
