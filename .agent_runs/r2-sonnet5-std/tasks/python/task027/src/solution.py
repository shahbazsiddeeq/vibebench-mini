def transpose(matrix):
    if not matrix or not matrix[0]:
        raise ValueError("matrix must be non-empty")

    row_length = len(matrix[0])
    for row in matrix:
        if len(row) != row_length:
            raise ValueError("all rows must have the same length")

    return [[row[i] for row in matrix] for i in range(row_length)]
