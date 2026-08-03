def linear_regression(xs, ys):
    """
    Fit a simple ordinary-least-squares line y = slope * x + intercept.
    
    Args:
        xs: list of x values
        ys: list of y values
    
    Returns:
        tuple (slope, intercept) rounded to 6 decimal places
    
    Raises:
        ValueError: if inputs are invalid
    """
    # Validate inputs
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    
    if len(xs) < 2:
        raise ValueError("Need at least 2 points")
    
    # Calculate means
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    
    # Calculate sums for slope
    sum_products = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sum_squares = sum((x - mx) ** 2 for x in xs)
    
    # Check for vertical line (all x values identical)
    if sum_squares == 0:
        raise ValueError("All x values are identical (undefined slope)")
    
    # Calculate slope and intercept
    slope = sum_products / sum_squares
    intercept = my - slope * mx
    
    # Round to 6 decimal places
    slope = round(slope, 6)
    intercept = round(intercept, 6)
    
    return (slope, intercept)
