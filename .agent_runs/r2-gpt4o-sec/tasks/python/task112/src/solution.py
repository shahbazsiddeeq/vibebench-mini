# src/solution.py

def matrix_multiply(a, b):
    # Validate inputs
    if not a or not b:
        raise ValueError("Input matrices cannot be empty.")
    
    if not all(isinstance(row, list) for row in a) or not all(isinstance(row, list) for row in b):
        raise ValueError("Both inputs must be 2D lists.")
    
    num_rows_a = len(a)
    num_cols_a = len(a[0])
    num_rows_b = len(b)
    num_cols_b = len(b[0])
    
    # Check if all rows in a have the same number of columns
    if any(len(row) != num_cols_a for row in a):
        raise ValueError("All rows in the first matrix must have the same number of columns.")
    
    # Check if all rows in b have the same number of columns
    if any(len(row) != num_cols_b for row in b):
        raise ValueError("All rows in the second matrix must have the same number of columns.")
    
    # Check if matrices can be multiplied
    if num_cols_a != num_rows_b:
        raise ValueError("Incompatible dimensions for matrix multiplication.")
    
    # Initialize result matrix with zeros
    result = [[0] * num_cols_b for _ in range(num_rows_a)]
    
    # Perform matrix multiplication
    for i in range(num_rows_a):
        for j in range(num_cols_b):
            for k in range(num_cols_a):
                result[i][j] += a[i][k] * b[k][j]
    
    return result
