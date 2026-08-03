import pytest
from src.solution import lcs_length


def test_identical():
    assert lcs_length("ABC", "ABC") == 3


def test_empty_first():
    assert lcs_length("", "ABC") == 0


def test_both_empty():
    assert lcs_length("", "") == 0


def test_single_char_no_match():
    assert lcs_length("A", "B") == 0
