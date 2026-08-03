from src.solution import long_lines
import pytest


def test_no_long_lines():
    source = "a\nb\nc\n"
    assert long_lines(source) == []


def test_one_over_limit_included():
    source = "x" * 80
    assert long_lines(source) == [1]


def test_multiple_long_lines():
    source = ("a" * 90) + "\nshort\n" + ("b" * 90)
    assert long_lines(source) == [1, 3]


def test_bare_cr_splits_lines():
    source = ("a" * 90) + "\r" + "short" + "\r" + ("b" * 90)
    assert long_lines(source) == [1, 3]


def test_form_feed_splits_lines():
    # Form feed (\x0c) ends line 1, so the long run becomes line 2.
    source = "abc\x0c" + ("x" * 80) + "\n"
    assert long_lines(source) == [2]
