from __future__ import annotations


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix or not matrix[0]:
        raise ValueError("matrix must be non-empty")
    row_len = len(matrix[0])
    if any(len(row) != row_len for row in matrix):
        raise ValueError("all rows must have the same length")
    return [list(row) for row in zip(*matrix)]
