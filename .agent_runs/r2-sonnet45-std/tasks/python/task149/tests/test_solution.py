import pytest

from src.solution import number_to_words


def test_zero():
    assert number_to_words(0) == "zero"


def test_single_digit():
    assert number_to_words(7) == "seven"


def test_teens():
    assert number_to_words(13) == "thirteen"
    assert number_to_words(19) == "nineteen"


def test_round_ten_not_hyphenated():
    assert number_to_words(40) == "forty"


def test_hyphenated_tens():
    assert number_to_words(42) == "forty-two"
    assert number_to_words(21) == "twenty-one"


def test_hundred_exact():
    assert number_to_words(100) == "one hundred"


def test_hundred_no_and():
    assert number_to_words(105) == "one hundred five"
    assert number_to_words(999) == "nine hundred ninety-nine"


def test_thousand_group():
    assert number_to_words(1234) == "one thousand two hundred thirty-four"


def test_exact_thousand():
    assert number_to_words(1000) == "one thousand"


def test_million():
    assert number_to_words(1000000) == "one million"


def test_billion_complex():
    assert number_to_words(2000001) == "two million one"


def test_negative():
    assert number_to_words(-42) == "negative forty-two"


def test_negative_large():
    assert number_to_words(-1000000) == "negative one million"


def test_max_value():
    assert number_to_words(999999999999) == (
        "nine hundred ninety-nine billion "
        "nine hundred ninety-nine million "
        "nine hundred ninety-nine thousand "
        "nine hundred ninety-nine"
    )


def test_no_leading_or_trailing_space():
    for v in (0, 5, 100, 1000, -73, 1000000, 999999999999):
        w = number_to_words(v)
        assert w == w.strip()


def test_out_of_range_high_raises():
    with pytest.raises(ValueError):
        number_to_words(1000000000000)


def test_out_of_range_low_raises():
    with pytest.raises(ValueError):
        number_to_words(-1000000000000)


def test_non_int_raises_typeerror():
    with pytest.raises(TypeError):
        number_to_words(3.0)
    with pytest.raises(TypeError):
        number_to_words("5")


def test_bool_rejected():
    with pytest.raises(TypeError):
        number_to_words(True)


def test_mutation_killer_skipped_zero_group():
    # 1,000,234 must NOT emit a spurious 'thousand'; the thousands group is zero.
    assert number_to_words(1000234) == "one million two hundred thirty-four"
