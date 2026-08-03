# src/solution.py

def matrix_multiply(a, b):
    # Validate inputs
    if not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("Both inputs must be lists.")
    
    if not a or not b:
        raise ValueError("Input matrices cannot be empty.")
    
    if not all(isinstance(row, list) for row in a) or not all(isinstance(row, list) for row in b):
        raise ValueError("Both inputs must be 2D lists.")
    
    if not all(len(row) == len(a[0]) for row in a):
        raise ValueError("All rows in the first matrix must have the same length.")
    
    if not all(len(row) == len(b[0]) for row in b):
        raise ValueError("All rows in the second matrix must have the same length.")
    
    if len(a[0]) != len(b):
        raise ValueError("Incompatible dimensions for matrix multiplication.")
    
    # Initialize the result matrix with zeros
    result = [[0] * len(b[0]) for _ in range(len(a))]
    
    # Perform matrix multiplication
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    
    return result
