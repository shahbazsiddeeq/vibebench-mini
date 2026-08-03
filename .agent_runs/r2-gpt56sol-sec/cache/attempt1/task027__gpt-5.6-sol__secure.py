"""Matrix transposition utilities."""

from typing import Any


def transpose(matrix: list[list[Any]]) -> list[list[Any]]:
    """Return the transpose of a rectangular, non-empty list of lists.

    Raises:
        ValueError: If the matrix is empty or has rows of different lengths.
        TypeError: If matrix is not a list of lists.
    """
    if not isinstance(matrix, list):
        raise TypeError("matrix must be a list of lists")
    if not matrix:
        raise ValueError("matrix must not be empty")
    if any(not isinstance(row, list) for row in matrix):
        raise TypeError("matrix must be a list of lists")

    column_count = len(matrix[0])
    if any(len(row) != column_count for row in matrix[1:]):
        raise ValueError("matrix rows must have equal lengths")

    return [
        [matrix[row_index][column_index] for row_index in range(len(matrix))]
        for column_index in range(column_count)
    ]
