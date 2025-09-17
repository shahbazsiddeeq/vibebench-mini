from src.solution import merge_intervals


def test_merge_basic():
    xs = [(1, 3), (2, 5), (7, 9), (9, 10)]
    assert merge_intervals(xs) == [(1, 5), (7, 10)]


def test_empty_and_sorted():
    assert merge_intervals([]) == []
    assert merge_intervals([(0, 1)]) == [(0, 1)]
