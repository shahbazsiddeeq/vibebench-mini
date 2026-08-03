def matrix_multiply(a, b):
    """Multiply two non-empty rectangular matrices.

    Raises:
        ValueError: If either matrix is empty, malformed, or their dimensions
            are incompatible.
    """
    if not isinstance(a, list) or not isinstance(b, list) or not a or not b:
        raise ValueError("matrices must be non-empty 2D lists")

    if not all(isinstance(row, list) and row for row in a):
        raise ValueError("first matrix must be rectangular and non-empty")
    if not all(isinstance(row, list) and row for row in b):
        raise ValueError("second matrix must be rectangular and non-empty")

    a_columns = len(a[0])
    b_columns = len(b[0])

    if any(len(row) != a_columns for row in a):
        raise ValueError("first matrix must be rectangular")
    if any(len(row) != b_columns for row in b):
        raise ValueError("second matrix must be rectangular")
    if a_columns != len(b):
        raise ValueError("matrix dimensions are incompatible")

    return [
        [
            sum(a[row][k] * b[k][column] for k in range(a_columns))
            for column in range(b_columns)
        ]
        for row in range(len(a))
    ]
