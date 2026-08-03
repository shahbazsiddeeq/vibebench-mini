import pytest
from src.solution import histogram


def test_edges_and_counts_exact():
    assert histogram([0, 1, 2, 3], 2) == [(0.0, 1.5, 2), (1.5, 3.0, 2)]


def test_single_bin():
    assert histogram([1.0, 2.0, 3.0], 1) == [(1.0, 3.0, 3)]


def test_invalid_bins():
    with pytest.raises(ValueError):
        histogram([1, 2, 3], 0)


def test_bin_ranges_cover_all():
    data = [1, 2, 3, 4, 5, 6]
    result = histogram(data, 3)
    assert len(result) == 3
    assert sum(c for _, _, c in result) == 6
    # bins are contiguous and start/end at the data extremes
    assert result[0][0] == 1.0
    assert result[-1][1] == 6.0
    for a, b in zip(result, result[1:]):
        assert a[1] == b[0]
