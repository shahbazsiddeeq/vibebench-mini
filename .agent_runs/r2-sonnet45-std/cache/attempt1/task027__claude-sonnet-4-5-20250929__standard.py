def transpose(matrix):
    """
    Returns the transpose of a 2D rectangular list of lists.
    
    Args:
        matrix: A 2D list of lists representing a matrix
        
    Returns:
        The transposed matrix as a new list of lists
        
    Raises:
        ValueError: If matrix is empty or rows have different lengths
    """
    # Check if matrix is empty
    if not matrix:
        raise ValueError("Matrix is empty")
    
    # Check if first row is empty
    if not matrix[0]:
        raise ValueError("Matrix is empty")
    
    # Get the expected row length from the first row
    expected_length = len(matrix[0])
    
    # Check that all rows have the same length
    for row in matrix:
        if len(row) != expected_length:
            raise ValueError("All rows must have the same length")
    
    # Perform the transpose
    num_rows = len(matrix)
    num_cols = expected_length
    
    result = []
    for col_idx in range(num_cols):
        new_row = []
        for row_idx in range(num_rows):
            new_row.append(matrix[row_idx][col_idx])
        result.append(new_row)
    
    return result
