import pytest
from src.solution import rotate


def test_k_zero():
    assert rotate([1, 2, 3], 0) == [1, 2, 3]


def test_k_larger_than_length():
    assert rotate([1, 2, 3], 7) == [3, 1, 2]  # 7 % 3 == 1


def test_empty():
    assert rotate([], 3) == []


def test_input_not_modified():
    original = [1, 2, 3, 4, 5]
    snapshot = list(original)
    rotate(original, 2)
    assert original == snapshot


def test_large_negative_k():
    # -7 % 5 == 3 -> right rotation by 3
    assert rotate([1, 2, 3, 4, 5], -7) == [3, 4, 5, 1, 2]
