from src.solution import long_lines
import pytest


def test_basic():
    source = "short\n" + ("x" * 100) + "\nalso short\n"
    assert long_lines(source) == [2]


def test_exact_limit_not_included():
    source = "x" * 79
    assert long_lines(source) == []


def test_custom_limit():
    source = "abc\nabcde\n"
    assert long_lines(source, limit=3) == [2]


def test_crlf_line_endings():
    # "\r\n" is a single terminator: line 1 is 80 chars (long), line 2 short.
    source = ("x" * 80) + "\r\n" + "short\r\n"
    assert long_lines(source) == [1]


def test_tab_counts_as_one_character():
    # 80 tab characters form a single 80-char line (tabs are not line breaks).
    assert long_lines("\t" * 80) == [1]
    # 79 tabs is exactly at the limit and is not reported.
    assert long_lines("\t" * 79) == []


def test_invalid_limit_raises():
    with pytest.raises(ValueError):
        long_lines("abc", limit=0)
