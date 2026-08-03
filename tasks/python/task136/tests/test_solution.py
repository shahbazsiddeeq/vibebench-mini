from src.solution import long_lines
import pytest


def test_basic():
    source = "short\n" + ("x" * 100) + "\nalso short\n"
    assert long_lines(source) == [2]


def test_no_long_lines():
    source = "a\nb\nc\n"
    assert long_lines(source) == []


def test_exact_limit_not_included():
    source = "x" * 79
    assert long_lines(source) == []


def test_one_over_limit_included():
    source = "x" * 80
    assert long_lines(source) == [1]


def test_custom_limit():
    source = "abc\nabcde\n"
    assert long_lines(source, limit=3) == [2]


def test_multiple_long_lines():
    source = ("a" * 90) + "\nshort\n" + ("b" * 90)
    assert long_lines(source) == [1, 3]


def test_crlf_line_endings():
    # "\r\n" is a single terminator: line 1 is 80 chars (long), line 2 short.
    source = ("x" * 80) + "\r\n" + "short\r\n"
    assert long_lines(source) == [1]


def test_bare_cr_splits_lines():
    source = ("a" * 90) + "\r" + "short" + "\r" + ("b" * 90)
    assert long_lines(source) == [1, 3]


def test_tab_counts_as_one_character():
    # 80 tab characters form a single 80-char line (tabs are not line breaks).
    assert long_lines("\t" * 80) == [1]
    # 79 tabs is exactly at the limit and is not reported.
    assert long_lines("\t" * 79) == []


def test_form_feed_splits_lines():
    # Form feed (\x0c) ends line 1, so the long run becomes line 2.
    source = "abc\x0c" + ("x" * 80) + "\n"
    assert long_lines(source) == [2]


def test_invalid_limit_raises():
    with pytest.raises(ValueError):
        long_lines("abc", limit=0)
