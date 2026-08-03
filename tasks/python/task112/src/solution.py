def matrix_multiply(a: list[list], b: list[list]) -> list[list]:
    if not a or not b or not a[0] or not b[0]:
        raise ValueError("Matrices must not be empty")
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    if cols_a != rows_b:
        raise ValueError(
            f"Incompatible dimensions: ({rows_a}x{cols_a}) @ ({rows_b}x{cols_b})"
        )
    return [
        [sum(a[i][k] * b[k][j] for k in range(cols_a)) for j in range(cols_b)]
        for i in range(rows_a)
    ]
