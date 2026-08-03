def matrix_multiply(a, b):
    if not a or not b or not a[0] or not b[0]:
        raise ValueError("Inputs must be non-empty matrices")

    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])

    if any(len(row) != cols_a for row in a):
        raise ValueError("Matrix a has inconsistent row lengths")
    if any(len(row) != cols_b for row in b):
        raise ValueError("Matrix b has inconsistent row lengths")

    if cols_a != rows_b:
        raise ValueError("Incompatible dimensions for matrix multiplication")

    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            total = 0
            for k in range(cols_a):
                total += a[i][k] * b[k][j]
            result[i][j] = total

    return result
