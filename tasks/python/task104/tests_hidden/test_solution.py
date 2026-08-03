from src.solution import Sorter, bubble_sort, insertion_sort


def test_bubble_sort():
    s = Sorter(bubble_sort)
    assert s.sort([3, 1, 2]) == [1, 2, 3]


def test_swap_strategy():
    s = Sorter(bubble_sort)
    s.set_strategy(insertion_sort)
    assert s.sort([4, 2, 3]) == [2, 3, 4]


def test_single():
    s = Sorter(insertion_sort)
    assert s.sort([7]) == [7]


def test_returns_new_list_object():
    original = [3, 1, 2]
    for strategy in (bubble_sort, insertion_sort):
        s = Sorter(strategy)
        result = s.sort(original)
        assert result is not original
        assert original == [3, 1, 2]


def test_standalone_functions_do_not_mutate():
    data = [4, 2, 3, 1]
    assert bubble_sort(data) == [1, 2, 3, 4]
    assert data == [4, 2, 3, 1]
    assert insertion_sort(data) == [1, 2, 3, 4]
    assert data == [4, 2, 3, 1]
