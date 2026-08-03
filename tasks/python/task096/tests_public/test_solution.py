import pytest
from src.solution import moving_average


def test_window_one():
    assert moving_average([1, 2, 3], 1) == [1.0, 2.0, 3.0]


def test_window_zero_raises():
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)


def test_output_length():
    data = list(range(10))
    result = moving_average(data, 3)
    assert len(result) == len(data) - 3 + 1
