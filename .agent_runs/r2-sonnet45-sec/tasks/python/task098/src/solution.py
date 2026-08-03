def pearson_r(x, y):
    """
    Calculate the Pearson correlation coefficient between two lists.
    
    Args:
        x: First list of numeric values
        y: Second list of numeric values
    
    Returns:
        float: Pearson correlation coefficient rounded to 4 decimal places
    
    Raises:
        ValueError: If lengths differ, fewer than 2 elements, or either has zero variance
    """
    # Validate inputs are lists or sequences
    if not hasattr(x, '__len__') or not hasattr(y, '__len__'):
        raise ValueError("Both inputs must be sequences")
    
    # Check lengths match
    if len(x) != len(y):
        raise ValueError("Input sequences must have the same length")
    
    # Check minimum length
    if len(x) < 2:
        raise ValueError("Input sequences must have at least 2 elements")
    
    # Validate all elements are numeric
    try:
        x_values = [float(val) for val in x]
        y_values = [float(val) for val in y]
    except (TypeError, ValueError):
        raise ValueError("All elements must be numeric")
    
    n = len(x_values)
    
    # Calculate means
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    
    # Calculate deviations and products
    sum_xy = 0.0
    sum_x_sq = 0.0
    sum_y_sq = 0.0
    
    for i in range(n):
        dx = x_values[i] - mean_x
        dy = y_values[i] - mean_y
        sum_xy += dx * dy
        sum_x_sq += dx * dx
        sum_y_sq += dy * dy
    
    # Check for zero variance
    if sum_x_sq == 0.0 or sum_y_sq == 0.0:
        raise ValueError("One or both sequences have zero variance")
    
    # Calculate Pearson correlation coefficient
    r = sum_xy / (sum_x_sq * sum_y_sq) ** 0.5
    
    # Round to 4 decimal places
    return round(r, 4)
