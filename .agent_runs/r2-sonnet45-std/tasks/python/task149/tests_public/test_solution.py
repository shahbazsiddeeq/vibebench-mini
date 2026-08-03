import pytest

from src.solution import number_to_words


def test_single_digit():
    assert number_to_words(7) == "seven"


def test_round_ten_not_hyphenated():
    assert number_to_words(40) == "forty"


def test_hundred_exact():
    assert number_to_words(100) == "one hundred"


def test_thousand_group():
    assert number_to_words(1234) == "one thousand two hundred thirty-four"


def test_million():
    assert number_to_words(1000000) == "one million"


def test_negative():
    assert number_to_words(-42) == "negative forty-two"


def test_max_value():
    assert number_to_words(999999999999) == (
        "nine hundred ninety-nine billion "
        "nine hundred ninety-nine million "
        "nine hundred ninety-nine thousand "
        "nine hundred ninety-nine"
    )


def test_out_of_range_high_raises():
    with pytest.raises(ValueError):
        number_to_words(1000000000000)


def test_non_int_raises_typeerror():
    with pytest.raises(TypeError):
        number_to_words(3.0)
    with pytest.raises(TypeError):
        number_to_words("5")


def test_mutation_killer_skipped_zero_group():
    # 1,000,234 must NOT emit a spurious 'thousand'; the thousands group is zero.
    assert number_to_words(1000234) == "one million two hundred thirty-four"
