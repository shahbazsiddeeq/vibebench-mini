import pytest
from src.solution import describe


def test_empty_raises():
    with pytest.raises(ValueError):
        describe([])


def test_range():
    result = describe([1, 5])
    assert result["range"] == 4


def test_std_dev_nonnegative():
    result = describe([1, 2, 3, 4, 5])
    assert result["std_dev"] >= 0


def test_mode_most_frequent():
    result = describe([1, 2, 2, 3, 3, 3])
    assert result["mode"] == 3


def test_population_std_dev_rounded():
    result = describe([1, 2, 2, 3])
    assert result["std_dev"] == 0.7071
