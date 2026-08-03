# src/solution.py

def matrix_multiply(a, b):
    if not a or not b or not a[0] or not b[0]:
        raise ValueError("Input matrices must not be empty.")
    
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    
    if cols_a != rows_b:
        raise ValueError("Incompatible dimensions for matrix multiplication.")
    
    # Initialize the result matrix with zeros
    result = [[0] * cols_b for _ in range(rows_a)]
    
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    
    return result
