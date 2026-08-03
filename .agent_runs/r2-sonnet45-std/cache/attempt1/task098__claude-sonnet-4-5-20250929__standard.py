def pearson_r(x, y):
    """
    Calculate the Pearson correlation coefficient between two lists.
    
    Args:
        x: First list of numbers
        y: Second list of numbers
    
    Returns:
        Pearson correlation coefficient rounded to 4 decimal places
    
    Raises:
        ValueError: If lengths differ, fewer than 2 elements, or either has zero variance
    """
    # Check if lengths differ
    if len(x) != len(y):
        raise ValueError("Lists must have the same length")
    
    # Check if fewer than 2 elements
    if len(x) < 2:
        raise ValueError("Lists must have at least 2 elements")
    
    n = len(x)
    
    # Calculate means
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    # Calculate deviations and products
    deviations_x = [xi - mean_x for xi in x]
    deviations_y = [yi - mean_y for yi in y]
    
    # Calculate sum of products of deviations
    sum_product = sum(dx * dy for dx, dy in zip(deviations_x, deviations_y))
    
    # Calculate sum of squared deviations
    sum_sq_x = sum(dx ** 2 for dx in deviations_x)
    sum_sq_y = sum(dy ** 2 for dy in deviations_y)
    
    # Check for zero variance
    if sum_sq_x == 0 or sum_sq_y == 0:
        raise ValueError("Lists must have non-zero variance")
    
    # Calculate Pearson correlation coefficient
    r = sum_product / (sum_sq_x ** 0.5 * sum_sq_y ** 0.5)
    
    # Round to 4 decimal places
    return round(r, 4)
