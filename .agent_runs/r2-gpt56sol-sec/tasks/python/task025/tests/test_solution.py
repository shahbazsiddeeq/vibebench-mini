import pytest
from src.solution import rotate


def test_basic_right():
    assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]


def test_k_zero():
    assert rotate([1, 2, 3], 0) == [1, 2, 3]


def test_k_equals_length():
    assert rotate([1, 2, 3], 3) == [1, 2, 3]


def test_k_larger_than_length():
    assert rotate([1, 2, 3], 7) == [3, 1, 2]  # 7 % 3 == 1


def test_k_negative():
    assert rotate([1, 2, 3, 4, 5], -2) == [3, 4, 5, 1, 2]


def test_empty():
    assert rotate([], 3) == []


def test_single_element():
    assert rotate([42], 5) == [42]


def test_input_not_modified():
    original = [1, 2, 3, 4, 5]
    snapshot = list(original)
    rotate(original, 2)
    assert original == snapshot


def test_returns_new_list():
    original = [1, 2, 3]
    result = rotate(original, 0)
    assert result == [1, 2, 3]
    assert result is not original
    result[0] = 99
    assert original == [1, 2, 3]


def test_large_negative_k():
    # -7 % 5 == 3 -> right rotation by 3
    assert rotate([1, 2, 3, 4, 5], -7) == [3, 4, 5, 1, 2]


@pytest.mark.parametrize(
    "lst,k,expected",
    [
        ([1, 2, 3, 4], 1, [4, 1, 2, 3]),
        ([1, 2, 3, 4], 4, [1, 2, 3, 4]),
    ],
)
def test_parametrized(lst, k, expected):
    assert rotate(lst, k) == expected
