import numbers

def matrix_multiply(a, b):
    """
    Multiplies two 2D lists (matrices) and returns the result.

    Args:
        a: The first matrix, a list of lists of numbers.
        b: The second matrix, a list of lists of numbers.

    Returns:
        A new list of lists representing the product of the two matrices.

    Raises:
        ValueError: If dimensions are incompatible, inputs are empty,
                    or inputs contain non-numeric values or non-rectangular shapes.
    """
    if not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("Inputs must be lists.")
    if not a or not b:
        raise ValueError("Input matrices cannot be empty.")

    rows_a = len(a)
    if not all(isinstance(row, list) for row in a):
        raise ValueError("Matrix A must contain only lists (rows).")
    if not all(row for row in a):
        raise ValueError("Matrix A rows cannot be empty.")
    cols_a = len(a[0])
    if not all(len(row) == cols_a for row in a):
        raise ValueError("Matrix A must be rectangular.")
    if not all(isinstance(val, numbers.Number) for row in a for val in row):
        raise ValueError("Matrix A must contain only numeric values.")

    rows_b = len(b)
    if not all(isinstance(row, list) for row in b):
        raise ValueError("Matrix B must contain only lists (rows).")
    if not all(row for row in b):
        raise ValueError("Matrix B rows cannot be empty.")
    cols_b = len(b[0])
    if not all(len(row) == cols_b for row in b):
        raise ValueError("Matrix B must be rectangular.")
    if not all(isinstance(val, numbers.Number) for row in b for val in row):
        raise ValueError("Matrix B must contain only numeric values.")

    if cols_a != rows_b:
        raise ValueError("Incompatible matrix dimensions for multiplication.")

    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):  # or rows_b, they are equal
                result[i][j] += a[i][k] * b[k][j]
    return result
