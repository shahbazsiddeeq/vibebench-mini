def transpose(matrix):
    """
    Transposes a 2D rectangular list of lists.

    Args:
        matrix: A list of lists representing a 2D matrix.

    Returns:
        A new list of lists representing the transpose of the input matrix.

    Raises:
        ValueError: If the matrix is empty or if rows have different lengths (jagged matrix).
    """
    if not matrix:
        raise ValueError("Matrix cannot be empty.")

    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Validate that all rows have the same length
    for i, row in enumerate(matrix):
        if not isinstance(row, list):
            raise ValueError(f"Matrix row at index {i} is not a list.")
        if len(row) != num_cols:
            raise ValueError("All rows in the matrix must have the same length.")

    # Create a new matrix for the transpose
    # Initialize with None or a default value, then fill
    transposed_matrix = [[None for _ in range(num_rows)] for _ in range(num_cols)]

    for r_idx in range(num_rows):
        for c_idx in range(num_cols):
            transposed_matrix[c_idx][r_idx] = matrix[r_idx][c_idx]

    return transposed_matrix
