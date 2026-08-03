import pytest
from src.solution import z_scores


def test_basic():
    result = z_scores([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    expected = [-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
    assert result == pytest.approx(expected, abs=1e-9)
    assert abs(sum(result)) < 1e-9


def test_known_values():
    result = z_scores([10.0, 20.0, 30.0])
    assert abs(result[0] - (-1.2247448)) < 1e-5
    assert abs(result[1] - 0.0) < 1e-9
    assert abs(result[2] - 1.2247448) < 1e-5


def test_zero_std():
    with pytest.raises(ValueError):
        z_scores([3.0, 3.0, 3.0])
