def matrix_multiply(a, b):
    """
    Multiplies two 2D matrices and returns the result.
    
    Args:
        a: First matrix (2D list)
        b: Second matrix (2D list)
    
    Returns:
        Result of matrix multiplication (2D list)
    
    Raises:
        ValueError: If dimensions are incompatible or inputs are empty
    """
    # Validate inputs are not empty
    if not a or not b:
        raise ValueError("Input matrices cannot be empty")
    
    # Validate that inputs are lists
    if not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("Inputs must be lists")
    
    # Validate that all rows exist and are lists
    if not all(isinstance(row, list) for row in a):
        raise ValueError("First matrix must be a 2D list")
    
    if not all(isinstance(row, list) for row in b):
        raise ValueError("Second matrix must be a 2D list")
    
    # Check for empty rows
    if any(not row for row in a):
        raise ValueError("First matrix cannot have empty rows")
    
    if any(not row for row in b):
        raise ValueError("Second matrix cannot have empty rows")
    
    # Get dimensions
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])
    
    # Validate all rows in first matrix have same length
    if not all(len(row) == cols_a for row in a):
        raise ValueError("All rows in first matrix must have same length")
    
    # Validate all rows in second matrix have same length
    if not all(len(row) == cols_b for row in b):
        raise ValueError("All rows in second matrix must have same length")
    
    # Check dimension compatibility: cols of a must equal rows of b
    if cols_a != rows_b:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    
    # Validate all elements are numbers
    for row in a:
        for elem in row:
            if not isinstance(elem, (int, float)) or isinstance(elem, bool):
                raise ValueError("Matrix elements must be numbers")
    
    for row in b:
        for elem in row:
            if not isinstance(elem, (int, float)) or isinstance(elem, bool):
                raise ValueError("Matrix elements must be numbers")
    
    # Perform matrix multiplication
    result = []
    for i in range(rows_a):
        result_row = []
        for j in range(cols_b):
            # Calculate dot product of row i from a and column j from b
            sum_val = 0
            for k in range(cols_a):
                sum_val += a[i][k] * b[k][j]
            result_row.append(sum_val)
        result.append(result_row)
    
    return result
