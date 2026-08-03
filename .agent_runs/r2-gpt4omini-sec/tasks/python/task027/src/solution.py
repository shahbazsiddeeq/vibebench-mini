# src/solution.py

def transpose(matrix):
    # Validate input
    if not isinstance(matrix, list):
        raise ValueError("Input must be a list of lists.")
    
    if not matrix:
        raise ValueError("Matrix cannot be empty.")
    
    row_length = len(matrix[0])
    
    for row in matrix:
        if not isinstance(row, list):
            raise ValueError("Each row must be a list.")
        if len(row) != row_length:
            raise ValueError("All rows must have the same length.")
    
    # Transpose the matrix
    transposed = []
    for i in range(row_length):
        new_row = []
        for row in matrix:
            new_row.append(row[i])
        transposed.append(new_row)
    
    return transposed
