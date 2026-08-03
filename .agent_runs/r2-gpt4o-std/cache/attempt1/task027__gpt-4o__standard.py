def transpose(matrix):
    if not matrix or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("Matrix is empty or rows have different lengths.")
    
    return [[matrix[row][col] for row in range(len(matrix))] for col in range(len(matrix[0]))]
