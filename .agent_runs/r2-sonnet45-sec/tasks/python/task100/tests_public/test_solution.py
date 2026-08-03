import pytest
from src.solution import freq_dist


def test_strings():
    assert freq_dist(["a", "b", "a"]) == {"a": 0.6667, "b": 0.3333}


def test_rounding_to_4dp():
    # 1/3 rounds to 0.3333, not a raw count and not full precision.
    result = freq_dist(["x", "y", "z"])
    assert result == {"x": 0.3333, "y": 0.3333, "z": 0.3333}


def test_single():
    assert freq_dist([42]) == {42: 1.0}
