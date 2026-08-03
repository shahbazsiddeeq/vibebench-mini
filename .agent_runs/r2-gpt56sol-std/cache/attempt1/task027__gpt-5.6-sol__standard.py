def transpose(matrix):
    """Return the transpose of a rectangular list of lists.

    Raises:
        ValueError: If the matrix is empty or its rows have different lengths.
    """
    if not matrix:
        raise ValueError("matrix must not be empty")

    column_count = len(matrix[0])
    if any(len(row) != column_count for row in matrix):
        raise ValueError("matrix rows must have equal lengths")

    return [[row[column] for row in matrix] for column in range(column_count)]
