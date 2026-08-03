"""
Matrix multiplication module.

Provides a secure, well-validated implementation of 2D matrix
multiplication using only the Python standard library.
"""

from numbers import Number
from typing import List, Sequence, Union

Number_T = Union[int, float]
Matrix = List[List[Number_T]]


def _validate_matrix(matrix: Sequence, name: str) -> None:
    """
    Validate that `matrix` is a non-empty, well-formed 2D list of numbers.

    Raises ValueError for any structural or type issue, without exposing
    internal details beyond a generic, safe message.
    """
    if not isinstance(matrix, list):
        raise ValueError(f"{name} must be a list of lists")

    if len(matrix) == 0:
        raise ValueError(f"{name} must not be empty")

    row_length = None
    for row in matrix:
        if not isinstance(row, list):
            raise ValueError(f"{name} must be a list of lists")
        if len(row) == 0:
            raise ValueError(f"{name} rows must not be empty")
        if row_length is None:
            row_length = len(row)
        elif len(row) != row_length:
            raise ValueError(f"{name} rows must all have the same length")
        for value in row:
            if isinstance(value, bool) or not isinstance(value, Number):
                raise ValueError(f"{name} must contain only numeric values")


def matrix_multiply(a: Sequence, b: Sequence) -> Matrix:
    """
    Multiply two 2D matrices `a` and `b` and return the resulting matrix.

    Raises:
        ValueError: if either matrix is empty, malformed (not a proper
            rectangular list of lists of numbers), or if their dimensions
            are incompatible for multiplication.
    """
    _validate_matrix(a, "First matrix")
    _validate_matrix(b, "Second matrix")

    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])

    if cols_a != rows_b:
        raise ValueError(
            "Incompatible dimensions for matrix multiplication"
        )

    result: Matrix = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        row_a = a[i]
        for k in range(cols_a):
            a_ik = row_a[k]
            if a_ik == 0:
                continue
            row_b = b[k]
            result_row = result[i]
            for j in range(cols_b):
                result_row[j] += a_ik * row_b[j]

    return result
