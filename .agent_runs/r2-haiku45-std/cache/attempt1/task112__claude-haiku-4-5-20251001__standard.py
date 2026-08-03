def matrix_multiply(a, b):
    """
    Multiplies two 2D matrices and returns the result.
    
    Args:
        a: First matrix (list of lists)
        b: Second matrix (list of lists)
    
    Returns:
        Result matrix (list of lists)
    
    Raises:
        ValueError: If dimensions are incompatible or inputs are empty
    """
    # Check if inputs are empty
    if not a or not b:
        raise ValueError("Input matrices cannot be empty")
    
    # Check if a is a valid matrix (all rows have same length)
    if not all(isinstance(row, list) for row in a):
        raise ValueError("First matrix must be a list of lists")
    
    if not all(isinstance(row, list) for row in b):
        raise ValueError("Second matrix must be a list of lists")
    
    # Get dimensions
    rows_a = len(a)
    cols_a = len(a[0]) if a else 0
    rows_b = len(b)
    cols_b = len(b[0]) if b else 0
    
    # Validate that all rows have consistent length
    for row in a:
        if len(row) != cols_a:
            raise ValueError("All rows in first matrix must have the same length")
    
    for row in b:
        if len(row) != cols_b:
            raise ValueError("All rows in second matrix must have the same length")
    
    # Check dimension compatibility: cols_a must equal rows_b
    if cols_a != rows_b:
        raise ValueError(f"Incompatible dimensions: ({rows_a}x{cols_a}) and ({rows_b}x{cols_b})")
    
    # Perform matrix multiplication
    result = []
    for i in range(rows_a):
        result_row = []
        for j in range(cols_b):
            # Calculate dot product of row i from a and column j from b
            dot_product = sum(a[i][k] * b[k][j] for k in range(cols_a))
            result_row.append(dot_product)
        result.append(result_row)
    
    return result
