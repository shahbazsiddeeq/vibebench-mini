import pytest
from src.solution import tokenize


def test_basic():
    assert tokenize("3 + 4.5 * (2-1)") == [3, "+", 4.5, "*", "(", 2, "-", 1, ")"]


def test_integers_only():
    assert tokenize("10 + 20") == [10, "+", 20]


def test_floats():
    assert tokenize("1.5 * 2.0") == [1.5, "*", 2.0]


def test_no_spaces():
    assert tokenize("1+2") == [1, "+", 2]


def test_empty():
    assert tokenize("") == []


def test_invalid_char():
    with pytest.raises(ValueError):
        tokenize("1 $ 2")


def test_int_and_float_types_preserved():
    tokens = tokenize("3 + 4.5")
    assert type(tokens[0]) is int and tokens[0] == 3
    assert type(tokens[2]) is float and tokens[2] == 4.5


def test_integer_is_not_float():
    (tok,) = tokenize("2")
    assert type(tok) is int


def test_whole_valued_float_stays_float():
    (tok,) = tokenize("2.0")
    assert type(tok) is float


def test_caret_and_percent_operators():
    assert tokenize("2 ^ 3 % 4") == [2, "^", 3, "%", 4]
