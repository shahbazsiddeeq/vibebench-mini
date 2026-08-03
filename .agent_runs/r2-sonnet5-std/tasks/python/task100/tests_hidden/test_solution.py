import pytest
from src.solution import freq_dist


def test_basic():
    assert freq_dist([1, 2, 2, 3, 3, 3]) == {1: 0.1667, 2: 0.3333, 3: 0.5}


def test_relative_frequencies_sum_to_one():
    result = freq_dist([1, 2, 3, 4])
    assert result == {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25}
    assert abs(sum(result.values()) - 1.0) < 1e-9


def test_empty_raises():
    with pytest.raises(ValueError):
        freq_dist([])


def test_all_same():
    assert freq_dist([7, 7, 7]) == {7: 1.0}
