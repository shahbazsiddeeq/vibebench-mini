import pytest
from src.solution import z_scores


def test_simple_two_point():
    result = z_scores([0.0, 2.0])
    assert abs(result[0] - (-1.0)) < 1e-9
    assert abs(result[1] - 1.0) < 1e-9


def test_too_few_points():
    with pytest.raises(ValueError):
        z_scores([5.0])
