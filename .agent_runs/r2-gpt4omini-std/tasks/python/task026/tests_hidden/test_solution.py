import pytest
from src.solution import permutations


def test_empty_list():
    assert permutations([]) == [()]


def test_two_elements():
    assert permutations([1, 2]) == [(1, 2), (2, 1)]


def test_unsorted_input_sorted_output():
    assert permutations([3, 1, 2]) == [
        (1, 2, 3),
        (1, 3, 2),
        (2, 1, 3),
        (2, 3, 1),
        (3, 1, 2),
        (3, 2, 1),
    ]


def test_too_large_raises():
    with pytest.raises(ValueError):
        permutations(list(range(9)))


def test_strings():
    assert permutations(["b", "a"]) == [("a", "b"), ("b", "a")]
