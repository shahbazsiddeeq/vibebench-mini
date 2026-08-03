"""Matrix multiplication utilities."""

from numbers import Number
from typing import List


def _validate_matrix(matrix: object, name: str) -> tuple[int, int]:
    """Validate a non-empty, rectangular numeric matrix."""
    if not isinstance(matrix, list) or not matrix:
        raise ValueError(f"{name} must be a non-empty 2D list")

    if not all(isinstance(row, list) and row for row in matrix):
        raise ValueError(f"{name} must contain non-empty rows")

    column_count = len(matrix[0])
    if any(len(row) != column_count for row in matrix):
        raise ValueError(f"{name} must be rectangular")

    if any(not isinstance(value, Number) for row in matrix for value in row):
        raise ValueError(f"{name} must contain only numeric values")

    return len(matrix), column_count


def matrix_multiply(a: list, b: list) -> List[List[Number]]:
    """Multiply two non-empty rectangular matrices.

    Raises:
        ValueError: If either input is invalid or their dimensions are
            incompatible.
    """
    rows_a, columns_a = _validate_matrix(a, "a")
    rows_b, columns_b = _validate_matrix(b, "b")

    if columns_a != rows_b:
        raise ValueError("matrix dimensions are incompatible")

    result: List[List[Number]] = []
    try:
        for row_index in range(rows_a):
            result_row = []
            for column_index in range(columns_b):
                value = sum(
                    a[row_index][index] * b[index][column_index]
                    for index in range(columns_a)
                )
                result_row.append(value)
            result.append(result_row)
    except (TypeError, ValueError, ArithmeticError):
        raise ValueError("matrix elements cannot be multiplied") from None

    return result
