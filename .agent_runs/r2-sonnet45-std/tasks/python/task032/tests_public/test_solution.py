import pytest
from src.solution import sliding_max


def test_window_one():
    assert sliding_max([1, 2, 3], 1) == [1, 2, 3]


def test_all_same():
    assert sliding_max([5, 5, 5, 5], 2) == [5, 5, 5]


def test_increasing():
    assert sliding_max([1, 2, 3, 4], 2) == [2, 3, 4]


def test_k_too_large_raises():
    with pytest.raises(ValueError):
        sliding_max([1, 2], 3)
