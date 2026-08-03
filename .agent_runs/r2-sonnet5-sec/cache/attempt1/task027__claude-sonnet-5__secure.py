"""
Matrix transpose utility module.

Provides a secure, well-validated implementation of a 2D matrix transpose
operation using only the Python standard library.
"""

from typing import List, Any


def transpose(matrix: List[List[Any]]) -> List[List[Any]]:
    """
    Return the transpose of a 2D rectangular list of lists.

    Args:
        matrix: A non-empty list of lists, where each inner list has the
            same length (a rectangular matrix).

    Returns:
        A new list of lists representing the transposed matrix. The
        returned structure does not share any references with the input.

    Raises:
        ValueError: If matrix is not a list, is empty, contains rows that
            are not lists, has rows of differing lengths, or has rows of
            length zero.
    """
    if not isinstance(matrix, list):
        raise ValueError("matrix must be a list of lists")

    if len(matrix) == 0:
        raise ValueError("matrix must not be empty")

    row_length = None
    for row in matrix:
        if not isinstance(row, list):
            raise ValueError("matrix must be a list of lists")
        if row_length is None:
            row_length = len(row)
            if row_length == 0:
                raise ValueError("matrix rows must not be empty")
        elif len(row) != row_length:
            raise ValueError("all rows must have the same length")

    # Build a brand-new structure; do not reuse any inner references.
    result: List[List[Any]] = [
        [matrix[row_idx][col_idx] for row_idx in range(len(matrix))]
        for col_idx in range(row_length)
    ]

    return result
