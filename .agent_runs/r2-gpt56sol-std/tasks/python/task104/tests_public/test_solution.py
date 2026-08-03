from src.solution import Sorter, bubble_sort, insertion_sort


def test_insertion_sort():
    s = Sorter(insertion_sort)
    assert s.sort([5, 3, 1, 4, 2]) == [1, 2, 3, 4, 5]


def test_empty():
    s = Sorter(bubble_sort)
    assert s.sort([]) == []


def test_does_not_mutate():
    original = [3, 1, 2]
    s = Sorter(bubble_sort)
    s.sort(original)
    assert original == [3, 1, 2]


def test_handles_duplicates_and_negatives():
    for strategy in (bubble_sort, insertion_sort):
        s = Sorter(strategy)
        assert s.sort([5, -1, 3, 3, -1, 0]) == [-1, -1, 0, 3, 3, 5]
