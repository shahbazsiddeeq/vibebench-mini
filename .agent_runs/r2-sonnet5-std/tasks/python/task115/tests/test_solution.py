from src.solution import merge_intervals


def test_overlapping():
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6],
        [8, 10],
        [15, 18],
    ]


def test_non_overlapping():
    assert merge_intervals([[1, 2], [3, 4]]) == [[1, 2], [3, 4]]


def test_all_overlap():
    assert merge_intervals([[1, 10], [2, 5], [3, 7]]) == [[1, 10]]


def test_single():
    assert merge_intervals([[1, 5]]) == [[1, 5]]


def test_empty():
    assert merge_intervals([]) == []


def test_unsorted():
    assert merge_intervals([[3, 4], [1, 2]]) == [[1, 2], [3, 4]]


def test_touching():
    assert merge_intervals([[1, 3], [3, 5]]) == [[1, 5]]
