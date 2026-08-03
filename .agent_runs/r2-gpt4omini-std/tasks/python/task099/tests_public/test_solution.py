import pytest
from src.solution import find_outliers


def test_finds_outliers():
    assert find_outliers([2, 2, 2, 2, 100], z_threshold=1.5) == [100]


def test_uses_population_std():
    # Population std (divide by N) gives z=2.0 for the 100; sample std (N-1)
    # gives ~1.79. A solution using sample std would return [] here.
    assert find_outliers([2, 2, 2, 2, 100], z_threshold=1.9) == [100]


def test_too_few_points():
    with pytest.raises(ValueError):
        find_outliers([5.0])


def test_constant_returns_empty():
    assert find_outliers([5, 5, 5, 5]) == []
