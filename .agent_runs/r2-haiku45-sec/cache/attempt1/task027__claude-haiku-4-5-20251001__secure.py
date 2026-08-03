def transpose(matrix):
    """
    Returns the transpose of a 2D rectangular list of lists.
    
    Args:
        matrix: A 2D list of lists to transpose
        
    Returns:
        A new transposed 2D list of lists
        
    Raises:
        ValueError: If matrix is empty or rows have different lengths
    """
    # Validate input is a list
    if not isinstance(matrix, list):
        raise ValueError("Matrix must be a list")
    
    # Check if matrix is empty
    if len(matrix) == 0:
        raise ValueError("Matrix cannot be empty")
    
    # Validate that all elements are lists
    for row in matrix:
        if not isinstance(row, list):
            raise ValueError("All rows must be lists")
    
    # Get the length of the first row
    first_row_length = len(matrix[0])
    
    # Check if first row is empty
    if first_row_length == 0:
        raise ValueError("Matrix rows cannot be empty")
    
    # Validate that all rows have the same length
    for row in matrix:
        if len(row) != first_row_length:
            raise ValueError("All rows must have the same length")
    
    # Create the transpose by iterating through columns
    # For each column index, create a new row with elements from that column
    transposed = []
    for col_idx in range(first_row_length):
        new_row = []
        for row_idx in range(len(matrix)):
            new_row.append(matrix[row_idx][col_idx])
        transposed.append(new_row)
    
    return transposed
