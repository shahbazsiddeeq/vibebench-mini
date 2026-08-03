import pytest

from src.solution import number_to_words


def test_zero():
    assert number_to_words(0) == "zero"


def test_teens():
    assert number_to_words(13) == "thirteen"
    assert number_to_words(19) == "nineteen"


def test_hyphenated_tens():
    assert number_to_words(42) == "forty-two"
    assert number_to_words(21) == "twenty-one"


def test_hundred_no_and():
    assert number_to_words(105) == "one hundred five"
    assert number_to_words(999) == "nine hundred ninety-nine"


def test_exact_thousand():
    assert number_to_words(1000) == "one thousand"


def test_billion_complex():
    assert number_to_words(2000001) == "two million one"


def test_negative_large():
    assert number_to_words(-1000000) == "negative one million"


def test_no_leading_or_trailing_space():
    for v in (0, 5, 100, 1000, -73, 1000000, 999999999999):
        w = number_to_words(v)
        assert w == w.strip()


def test_out_of_range_low_raises():
    with pytest.raises(ValueError):
        number_to_words(-1000000000000)


def test_bool_rejected():
    with pytest.raises(TypeError):
        number_to_words(True)
