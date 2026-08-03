import pytest
from src.solution import transpose


def test_square():
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]


def test_single_row():
    assert transpose([[1, 2, 3]]) == [[1], [2], [3]]


def test_empty_raises():
    with pytest.raises(ValueError):
        transpose([])


def test_3x3():
    m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert transpose(m) == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
