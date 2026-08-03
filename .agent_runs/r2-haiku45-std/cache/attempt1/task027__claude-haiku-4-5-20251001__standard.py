def transpose(matrix):
    """
    Returns the transpose of a 2D rectangular list of lists.
    
    Args:
        matrix: A 2D list of lists
        
    Returns:
        The transposed matrix as a new 2D list of lists
        
    Raises:
        ValueError: If matrix is empty or rows have different lengths
    """
    # Check if matrix is empty
    if not matrix:
        raise ValueError("Matrix cannot be empty")
    
    # Check if any row is empty
    if not matrix[0]:
        raise ValueError("Matrix cannot be empty")
    
    # Get the expected row length from the first row
    expected_length = len(matrix[0])
    
    # Check if all rows have the same length
    for row in matrix:
        if len(row) != expected_length:
            raise ValueError("All rows must have the same length")
    
    # Transpose the matrix using zip
    # zip(*matrix) unpacks the matrix rows and zips them together
    # We convert each zipped tuple to a list to create new lists
    transposed = [list(col) for col in zip(*matrix)]
    
    return transposed
