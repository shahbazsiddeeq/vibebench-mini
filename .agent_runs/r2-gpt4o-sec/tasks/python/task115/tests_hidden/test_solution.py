from src.solution import merge_intervals


def test_overlapping():
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6],
        [8, 10],
        [15, 18],
    ]


def test_all_overlap():
    assert merge_intervals([[1, 10], [2, 5], [3, 7]]) == [[1, 10]]


def test_empty():
    assert merge_intervals([]) == []


def test_touching():
    assert merge_intervals([[1, 3], [3, 5]]) == [[1, 5]]
