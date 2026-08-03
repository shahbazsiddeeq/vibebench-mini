def linear_regression(xs, ys):
    """
    Fit a simple ordinary-least-squares line y = slope * x + intercept
    to the paired data in lists xs and ys.
    
    Args:
        xs: List of x values
        ys: List of y values
        
    Returns:
        Tuple (slope, intercept) where each value is rounded to 6 decimal places
        
    Raises:
        ValueError: if xs and ys have different lengths, fewer than 2 points,
                   or if all x values are identical
    """
    # Check that xs and ys have the same length
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    
    # Check that there are at least 2 points
    if len(xs) < 2:
        raise ValueError("Must have at least 2 points")
    
    # Calculate means
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    
    # Calculate sum of products and sum of squares
    sum_products = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sum_squares = sum((x - mx) ** 2 for x in xs)
    
    # Check if all x values are identical
    if sum_squares == 0:
        raise ValueError("All x values are identical (undefined slope)")
    
    # Calculate slope and intercept
    slope = sum_products / sum_squares
    intercept = my - slope * mx
    
    # Round to 6 decimal places
    slope = round(slope, 6)
    intercept = round(intercept, 6)
    
    return (slope, intercept)
