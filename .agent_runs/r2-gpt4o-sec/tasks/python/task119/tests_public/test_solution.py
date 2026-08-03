import pytest
from src.solution import tokenize


def test_integers_only():
    assert tokenize("10 + 20") == [10, "+", 20]


def test_no_spaces():
    assert tokenize("1+2") == [1, "+", 2]


def test_invalid_char():
    with pytest.raises(ValueError):
        tokenize("1 $ 2")


def test_integer_is_not_float():
    (tok,) = tokenize("2")
    assert type(tok) is int


def test_caret_and_percent_operators():
    assert tokenize("2 ^ 3 % 4") == [2, "^", 3, "%", 4]
