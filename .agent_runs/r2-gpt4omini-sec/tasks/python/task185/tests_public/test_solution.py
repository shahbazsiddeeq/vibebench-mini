import pytest

from src.solution import find_mutable_defaults


def test_set_display_counts():
    assert find_mutable_defaults("def f(a={1, 2}):\n    pass") == [("f", 1)]


def test_call_defaults_do_not_count():
    # list() / dict() are calls, not literal displays.
    src = "def f(a=list(), b=dict()):\n    return a\n"
    assert find_mutable_defaults(src) == []


def test_reported_once_even_with_multiple():
    src = "def f(a=[], b={}, c={1}):\n    return a\n"
    assert find_mutable_defaults(src) == [("f", 1)]


def test_mutation_killer_string_and_comment_not_matched():
    # A naive text/regex scanner would flag these def(...=[]) fragments.
    src = (
        "s = 'def trap(a=[]):'\n"
        "# def trap2(b={}):\n"
        "def real(c=[]):\n"
        "    return s\n"
    )
    assert find_mutable_defaults(src) == [("real", 3)]


def test_sorted_by_line_then_name():
    src = (
        "def bbb(a=[]):\n"
        "    pass\n"
        "def aaa(b={}):\n"
        "    pass\n"
    )
    assert find_mutable_defaults(src) == [("bbb", 1), ("aaa", 3)]


def test_invalid_source_raises():
    with pytest.raises(ValueError):
        find_mutable_defaults("def f(:\n")
