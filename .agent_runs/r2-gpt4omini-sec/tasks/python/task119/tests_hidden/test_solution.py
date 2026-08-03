import pytest
from src.solution import tokenize


def test_basic():
    assert tokenize("3 + 4.5 * (2-1)") == [3, "+", 4.5, "*", "(", 2, "-", 1, ")"]


def test_floats():
    assert tokenize("1.5 * 2.0") == [1.5, "*", 2.0]


def test_empty():
    assert tokenize("") == []


def test_int_and_float_types_preserved():
    tokens = tokenize("3 + 4.5")
    assert type(tokens[0]) is int and tokens[0] == 3
    assert type(tokens[2]) is float and tokens[2] == 4.5


def test_whole_valued_float_stays_float():
    (tok,) = tokenize("2.0")
    assert type(tok) is float
