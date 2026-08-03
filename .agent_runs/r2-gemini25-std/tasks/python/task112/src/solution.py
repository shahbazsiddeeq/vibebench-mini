def matrix_multiply(a, b):
    """
    Multiplies two 2D lists (matrices) and returns the result.

    Args:
        a: The first matrix (list of lists).
        b: The second matrix (list of lists).

    Returns:
        The resulting matrix after multiplication.

    Raises:
        ValueError: If dimensions are incompatible or inputs are empty.
    """
    if not a or not b:
        raise ValueError("Input matrices cannot be empty.")

    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])

    # Check for empty rows in matrices
    if any(not row for row in a) or any(not row for row in b):
        raise ValueError("Input matrices cannot contain empty rows.")

    # Check for consistent row lengths in matrix a
    if any(len(row) != cols_a for row in a):
        raise ValueError("Matrix 'a' has inconsistent row lengths.")

    # Check for consistent row lengths in matrix b
    if any(len(row) != cols_b for row in b):
        raise ValueError("Matrix 'b' has inconsistent row lengths.")

    if cols_a != rows_b:
        raise ValueError("Incompatible matrix dimensions for multiplication.")

    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):  # or rows_b, they are equal
                result[i][j] += a[i][k] * b[k][j]

    return result
