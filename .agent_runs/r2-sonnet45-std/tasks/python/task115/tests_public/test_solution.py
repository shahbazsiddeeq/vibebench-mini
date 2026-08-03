from src.solution import merge_intervals


def test_non_overlapping():
    assert merge_intervals([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]


def test_single():
    assert merge_intervals([[1, 5]]) == [[1, 5]]


def test_unsorted():
    assert merge_intervals([[3, 4], [1, 2]]) == [[1, 2], [3, 4]]
