def transpose(matrix):
    """
    Returns the transpose of a 2D rectangular list of lists.
    
    Args:
        matrix: A 2D list of lists representing a matrix
        
    Returns:
        A new 2D list representing the transposed matrix
        
    Raises:
        ValueError: If matrix is empty or rows have different lengths
    """
    # Validate input type
    if not isinstance(matrix, list):
        raise ValueError("Matrix must be a list")
    
    # Check if matrix is empty
    if len(matrix) == 0:
        raise ValueError("Matrix cannot be empty")
    
    # Check if first row exists and is a list
    if not isinstance(matrix[0], list):
        raise ValueError("Matrix must be a list of lists")
    
    # Check if matrix has at least one element
    if len(matrix[0]) == 0:
        raise ValueError("Matrix rows cannot be empty")
    
    # Get the expected row length from the first row
    expected_length = len(matrix[0])
    
    # Validate all rows
    for i, row in enumerate(matrix):
        # Check that each row is a list
        if not isinstance(row, list):
            raise ValueError("Matrix must be a list of lists")
        
        # Check that all rows have the same length
        if len(row) != expected_length:
            raise ValueError("All rows must have the same length")
    
    # Perform transpose
    num_rows = len(matrix)
    num_cols = expected_length
    
    # Create new transposed matrix
    transposed = []
    for col_idx in range(num_cols):
        new_row = []
        for row_idx in range(num_rows):
            new_row.append(matrix[row_idx][col_idx])
        transposed.append(new_row)
    
    return transposed
