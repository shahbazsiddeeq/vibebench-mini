import pytest
from src.solution import moving_average


def test_basic():
    assert moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_window_full():
    assert moving_average([2, 4, 6], 3) == [4.0]


def test_window_too_large_raises():
    with pytest.raises(ValueError):
        moving_average([1, 2], 3)


@pytest.mark.parametrize(
    "data,w,expected",
    [
        ([1, 1, 1, 1], 2, [1.0, 1.0, 1.0]),
        ([10, 20, 30], 2, [15.0, 25.0]),
    ],
)
def test_parametrized(data, w, expected):
    assert moving_average(data, w) == expected
