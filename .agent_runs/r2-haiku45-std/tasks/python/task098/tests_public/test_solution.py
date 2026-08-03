import pytest
from src.solution import pearson_r


def test_perfect_negative():
    assert abs(pearson_r([1, 2, 3], [3, 2, 1]) + 1.0) < 1e-9


def test_known_correlation():
    r = pearson_r([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
    assert r == 0.7746


def test_negative_correlation():
    r = pearson_r([1, 2, 3, 4, 5], [10, 8, 6, 4, 2])
    assert r == -1.0


def test_length_mismatch():
    with pytest.raises(ValueError):
        pearson_r([1, 2], [1, 2, 3])
