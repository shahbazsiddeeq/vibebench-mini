import pytest
from src.solution import permutations


def test_empty_list():
    assert permutations([]) == [()]


def test_single_element():
    assert permutations([1]) == [(1,)]


def test_two_elements():
    assert permutations([1, 2]) == [(1, 2), (2, 1)]


def test_three_elements_exact():
    assert permutations([1, 2, 3]) == [
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1),
    ]


def test_unsorted_input_sorted_output():
    assert permutations([3, 1, 2]) == [
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1),
    ]


def test_duplicates_produce_duplicate_tuples():
    assert permutations([1, 1]) == [(1, 1), (1, 1)]
    assert permutations([2, 2, 2]) == [(2, 2, 2)] * 6


def test_too_large_raises():
    with pytest.raises(ValueError):
        permutations(list(range(9)))


def test_boundary_ok():
    result = permutations(list(range(8)))
    assert len(result) == 40320
    assert result == sorted(result)
    assert result[0] == (0, 1, 2, 3, 4, 5, 6, 7)
    assert result[-1] == (7, 6, 5, 4, 3, 2, 1, 0)


def test_strings():
    assert permutations(["b", "a"]) == [("a", "b"), ("b", "a")]
