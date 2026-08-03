# src/solution.py

def transpose(matrix):
    if not matrix:
        raise ValueError("Matrix is empty")
    
    row_length = len(matrix[0])
    for row in matrix:
        if len(row) != row_length:
            raise ValueError("Rows have different lengths")
    
    transposed = []
    for i in range(row_length):
        new_row = [matrix[j][i] for j in range(len(matrix))]
        transposed.append(new_row)
    
    return transposed
