def matrix_multiply(a, b):
    """
    Multiply two 2D matrices and return the result.
    
    Args:
        a: First matrix (2D list)
        b: Second matrix (2D list)
    
    Returns:
        Result of matrix multiplication (2D list)
    
    Raises:
        ValueError: If dimensions are incompatible or inputs are empty
    """
    # Check for empty inputs
    if not a or not b:
        raise ValueError("Input matrices cannot be empty")
    
    # Check if first matrix has empty rows
    if not a[0] or any(not row for row in a):
        raise ValueError("Input matrices cannot be empty")
    
    # Check if second matrix has empty rows
    if not b[0] or any(not row for row in b):
        raise ValueError("Input matrices cannot be empty")
    
    # Get dimensions
    m = len(a)  # rows in a
    n = len(a[0])  # cols in a
    p = len(b)  # rows in b
    q = len(b[0])  # cols in b
    
    # Verify all rows in a have same length
    if any(len(row) != n for row in a):
        raise ValueError("All rows in first matrix must have same length")
    
    # Verify all rows in b have same length
    if any(len(row) != q for row in b):
        raise ValueError("All rows in second matrix must have same length")
    
    # Check compatibility: cols of a must equal rows of b
    if n != p:
        raise ValueError("Incompatible dimensions for matrix multiplication")
    
    # Perform multiplication
    result = []
    for i in range(m):
        row = []
        for j in range(q):
            # Compute dot product of a[i] and column j of b
            value = sum(a[i][k] * b[k][j] for k in range(n))
            row.append(value)
        result.append(row)
    
    return result
