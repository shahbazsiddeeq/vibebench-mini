def matrix_multiply(a, b):
    """
    Multiplies two 2D matrices and returns the result.
    
    Args:
        a: First matrix as a 2D list
        b: Second matrix as a 2D list
    
    Returns:
        Result of matrix multiplication as a 2D list
    
    Raises:
        ValueError: If dimensions are incompatible or inputs are empty
    """
    # Validate inputs are not None
    if a is None or b is None:
        raise ValueError("Matrices cannot be None")
    
    # Validate inputs are lists
    if not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("Inputs must be lists")
    
    # Check for empty matrices
    if len(a) == 0 or len(b) == 0:
        raise ValueError("Matrices cannot be empty")
    
    # Validate that a is a proper 2D matrix
    if not all(isinstance(row, list) for row in a):
        raise ValueError("First matrix must be a 2D list")
    
    if not all(isinstance(row, list) for row in b):
        raise ValueError("Second matrix must be a 2D list")
    
    # Get dimensions of matrix a
    rows_a = len(a)
    cols_a = len(a[0]) if rows_a > 0 else 0
    
    # Validate all rows in a have the same length
    if not all(len(row) == cols_a for row in a):
        raise ValueError("All rows in first matrix must have the same length")
    
    # Get dimensions of matrix b
    rows_b = len(b)
    cols_b = len(b[0]) if rows_b > 0 else 0
    
    # Validate all rows in b have the same length
    if not all(len(row) == cols_b for row in b):
        raise ValueError("All rows in second matrix must have the same length")
    
    # Check dimension compatibility: cols_a must equal rows_b
    if cols_a != rows_b:
        raise ValueError(
            f"Incompatible dimensions: cannot multiply {rows_a}x{cols_a} "
            f"matrix with {rows_b}x{cols_b} matrix"
        )
    
    # Validate that all elements are numbers
    for row in a:
        for elem in row:
            if not isinstance(elem, (int, float)):
                raise ValueError("Matrix elements must be numbers")
    
    for row in b:
        for elem in row:
            if not isinstance(elem, (int, float)):
                raise ValueError("Matrix elements must be numbers")
    
    # Perform matrix multiplication
    result = []
    for i in range(rows_a):
        result_row = []
        for j in range(cols_b):
            # Calculate dot product of row i from a and column j from b
            dot_product = 0
            for k in range(cols_a):
                dot_product += a[i][k] * b[k][j]
            result_row.append(dot_product)
        result.append(result_row)
    
    return result
