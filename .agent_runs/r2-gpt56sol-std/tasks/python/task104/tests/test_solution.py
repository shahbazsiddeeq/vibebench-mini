from src.solution import Sorter, bubble_sort, insertion_sort


def test_bubble_sort():
    s = Sorter(bubble_sort)
    assert s.sort([3, 1, 2]) == [1, 2, 3]


def test_insertion_sort():
    s = Sorter(insertion_sort)
    assert s.sort([5, 3, 1, 4, 2]) == [1, 2, 3, 4, 5]


def test_swap_strategy():
    s = Sorter(bubble_sort)
    s.set_strategy(insertion_sort)
    assert s.sort([4, 2, 3]) == [2, 3, 4]


def test_empty():
    s = Sorter(bubble_sort)
    assert s.sort([]) == []


def test_single():
    s = Sorter(insertion_sort)
    assert s.sort([7]) == [7]


def test_does_not_mutate():
    original = [3, 1, 2]
    s = Sorter(bubble_sort)
    s.sort(original)
    assert original == [3, 1, 2]


def test_returns_new_list_object():
    original = [3, 1, 2]
    for strategy in (bubble_sort, insertion_sort):
        s = Sorter(strategy)
        result = s.sort(original)
        assert result is not original
        assert original == [3, 1, 2]


def test_handles_duplicates_and_negatives():
    for strategy in (bubble_sort, insertion_sort):
        s = Sorter(strategy)
        assert s.sort([5, -1, 3, 3, -1, 0]) == [-1, -1, 0, 3, 3, 5]


def test_standalone_functions_do_not_mutate():
    data = [4, 2, 3, 1]
    assert bubble_sort(data) == [1, 2, 3, 4]
    assert data == [4, 2, 3, 1]
    assert insertion_sort(data) == [1, 2, 3, 4]
    assert data == [4, 2, 3, 1]
