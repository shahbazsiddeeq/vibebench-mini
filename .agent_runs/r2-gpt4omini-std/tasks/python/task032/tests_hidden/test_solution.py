import pytest
from src.solution import sliding_max


def test_basic():
    assert sliding_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]


def test_window_full():
    assert sliding_max([3, 1, 2], 3) == [3]


def test_decreasing():
    assert sliding_max([5, 4, 3, 2], 2) == [5, 4, 3]


def test_k_zero_raises():
    with pytest.raises(ValueError):
        sliding_max([1, 2, 3], 0)
