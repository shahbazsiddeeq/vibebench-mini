def pearson_r(x, y):
    """
    Calculate the Pearson correlation coefficient between two sequences.
    
    Args:
        x: First sequence of numbers
        y: Second sequence of numbers
    
    Returns:
        Pearson correlation coefficient rounded to 4 decimal places
    
    Raises:
        ValueError: If lengths differ, fewer than 2 elements, or either has zero variance
    """
    # Convert to lists if needed
    x = list(x)
    y = list(y)
    
    # Check lengths match
    if len(x) != len(y):
        raise ValueError("Lengths of x and y must match")
    
    # Check minimum length
    if len(x) < 2:
        raise ValueError("Both sequences must have at least 2 elements")
    
    # Calculate means
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    
    # Calculate deviations and products
    deviations_x = [xi - mean_x for xi in x]
    deviations_y = [yi - mean_y for yi in y]
    
    # Calculate variances
    var_x = sum(d ** 2 for d in deviations_x)
    var_y = sum(d ** 2 for d in deviations_y)
    
    # Check for zero variance
    if var_x == 0 or var_y == 0:
        raise ValueError("Both sequences must have non-zero variance")
    
    # Calculate covariance
    covariance = sum(dx * dy for dx, dy in zip(deviations_x, deviations_y))
    
    # Calculate correlation coefficient
    r = covariance / (var_x * var_y) ** 0.5
    
    # Round to 4 decimal places
    return round(r, 4)
