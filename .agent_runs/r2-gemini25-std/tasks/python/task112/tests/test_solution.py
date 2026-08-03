import pytest
from src.solution import matrix_multiply


def test_2x2():
    assert matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]


def test_identity():
    assert matrix_multiply([[1, 2], [3, 4]], [[1, 0], [0, 1]]) == [[1, 2], [3, 4]]


def test_non_square():
    a = [[1, 2, 3]]
    b = [[1], [2], [3]]
    assert matrix_multiply(a, b) == [[14]]


def test_incompatible():
    with pytest.raises(ValueError):
        matrix_multiply([[1, 2]], [[1, 2]])


def test_rectangular_2x3_by_3x2():
    a = [[1, 2, 3], [4, 5, 6]]
    b = [[7, 8], [9, 10], [11, 12]]
    assert matrix_multiply(a, b) == [[58, 64], [139, 154]]


def test_rectangular_3x2_by_2x3():
    a = [[1, 2], [3, 4], [5, 6]]
    b = [[1, 2, 3], [4, 5, 6]]
    assert matrix_multiply(a, b) == [[9, 12, 15], [19, 26, 33], [29, 40, 51]]


def test_empty():
    with pytest.raises(ValueError):
        matrix_multiply([], [[1]])


def test_empty_second_operand():
    with pytest.raises(ValueError):
        matrix_multiply([[1]], [])
