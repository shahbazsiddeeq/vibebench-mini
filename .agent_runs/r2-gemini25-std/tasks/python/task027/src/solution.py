def transpose(matrix):
    """
    Returns the transpose of a 2D rectangular list of lists.

    Raises ValueError if matrix is empty or rows have different lengths.

    Args:
        matrix: A list of lists representing a 2D matrix.

    Returns:
        A new list of lists representing the transpose of the input matrix.
    """
    if not matrix:
        raise ValueError("Matrix cannot be empty.")

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Check for jagged rows
    for row in matrix:
        if len(row) != num_cols:
            raise ValueError("Rows in the matrix must have the same length.")

    # Create a new matrix for the transpose
    # Initialize with None or 0, then fill
    transposed_matrix = [[None for _ in range(num_rows)] for _ in range(num_cols)]

    for r_idx in range(num_rows):
        for c_idx in range(num_cols):
            transposed_matrix[c_idx][r_idx] = matrix[r_idx][c_idx]

    return transposed_matrix
