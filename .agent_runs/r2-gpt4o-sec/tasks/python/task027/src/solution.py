def transpose(matrix):
    if not matrix or not all(isinstance(row, list) for row in matrix):
        raise ValueError("Matrix must be a non-empty list of lists.")
    
    row_length = len(matrix[0])
    for row in matrix:
        if len(row) != row_length:
            raise ValueError("All rows must have the same length.")
    
    return [[matrix[row][col] for row in range(len(matrix))] for col in range(row_length)]
