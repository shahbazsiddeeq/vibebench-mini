import pytest
from src.solution import histogram


def test_example_exact_tuples():
    assert histogram([1, 2, 3, 4, 5], 2) == [(1.0, 3.0, 2), (3.0, 5.0, 3)]


def test_interior_edge_belongs_to_upper_bin():
    # 2.0 sits on the interior edge; half-open [0,2) excludes it, so it lands
    # in the upper bin.
    assert histogram([0, 2, 4], 2) == [(0.0, 2.0, 1), (2.0, 4.0, 2)]


def test_all_same():
    assert histogram([5, 5, 5], 3) == [(5.0, 5.0, 3)]


def test_empty_data():
    with pytest.raises(ValueError):
        histogram([], 3)
