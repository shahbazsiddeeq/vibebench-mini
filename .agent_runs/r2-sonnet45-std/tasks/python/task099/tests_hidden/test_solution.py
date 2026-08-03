import pytest
from src.solution import find_outliers


def test_no_outliers():
    assert find_outliers([1, 2, 3, 4, 5]) == []


def test_custom_threshold():
    assert find_outliers([1, 2, 3, 4, 5, 100], z_threshold=1.0) == [100]


def test_preserves_order_and_multiple():
    data = [-50, 0, 0, 0, 0, 0, 0, 0, 0, 50]
    assert find_outliers(data, z_threshold=2.0) == [-50, 50]


def test_empty_raises():
    with pytest.raises(ValueError):
        find_outliers([])
