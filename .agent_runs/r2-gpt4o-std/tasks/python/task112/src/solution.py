def matrix_multiply(a, b):
    if not a or not b or not a[0] or not b[0]:
        raise ValueError("Input matrices cannot be empty.")
    
    num_rows_a = len(a)
    num_cols_a = len(a[0])
    num_rows_b = len(b)
    num_cols_b = len(b[0])
    
    if num_cols_a != num_rows_b:
        raise ValueError("Incompatible dimensions for matrix multiplication.")
    
    result = [[0] * num_cols_b for _ in range(num_rows_a)]
    
    for i in range(num_rows_a):
        for j in range(num_cols_b):
            for k in range(num_cols_a):
                result[i][j] += a[i][k] * b[k][j]
    
    return result
