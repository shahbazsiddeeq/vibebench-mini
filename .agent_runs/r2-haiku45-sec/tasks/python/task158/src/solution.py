"""Linear regression implementation using ordinary least squares."""


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
    # Input validation
    if not isinstance(xs, (list, tuple)):
        raise ValueError("xs must be a list or tuple")
    if not isinstance(ys, (list, tuple)):
        raise ValueError("ys must be a list or tuple")
    
    # Check lengths match
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    
    # Check minimum number of points
    if len(xs) < 2:
        raise ValueError("At least 2 points are required")
    
    # Validate that all elements are numeric
    try:
        xs_float = [float(x) for x in xs]
        ys_float = [float(y) for y in ys]
    except (TypeError, ValueError):
        raise ValueError("All elements in xs and ys must be numeric")
    
    # Calculate means
    mx = sum(xs_float) / len(xs_float)
    my = sum(ys_float) / len(ys_float)
    
    # Calculate sum of products and sum of squares
    sum_products = sum((x - mx) * (y - my) for x, y in zip(xs_float, ys_float))
    sum_squares = sum((x - mx) ** 2 for x in xs_float)
    
    # Check for vertical line (undefined slope)
    if sum_squares == 0:
        raise ValueError("All x values are identical; slope is undefined")
    
    # Calculate slope and intercept
    slope = sum_products / sum_squares
    intercept = my - slope * mx
    
    # Round to 6 decimal places
    slope = round(slope, 6)
    intercept = round(intercept, 6)
    
    return (slope, intercept)
