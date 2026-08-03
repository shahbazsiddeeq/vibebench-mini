import pytest
from src.solution import is_balanced


def test_empty_string():
    assert is_balanced("") is True


def test_simple_parens():
    assert is_balanced("()") is True


def test_nested():
    assert is_balanced("([{}])") is True


def test_interleaved_invalid():
    assert is_balanced("([)]") is False


def test_unmatched_open():
    assert is_balanced("((") is False


def test_unmatched_close():
    assert is_balanced("))") is False


def test_wrong_close():
    assert is_balanced("(]") is False


def test_mixed_content_ignored():
    # Non-bracket characters are ignored; only bracket nesting matters.
    assert is_balanced("a(b)c[d]{e}") is True
    assert is_balanced("hello world") is True
    assert is_balanced("f(x) = y[0]") is True
    assert is_balanced("foo(bar]baz") is False
    assert is_balanced("code {") is False


def test_deeply_nested():
    assert is_balanced("(" * 1000 + ")" * 1000) is True
    assert is_balanced("([{" * 500 + "}])" * 500) is True
    assert is_balanced("(" * 1000 + ")" * 999) is False
    assert is_balanced("[" + "([{}])" * 500 + "]") is True


@pytest.mark.parametrize(
    "s,expected",
    [
        ("{[]}", True),
        ("{[}", False),
        ("[](){}", True),
        ("][", False),
    ],
)
def test_parametrized(s, expected):
    assert is_balanced(s) == expected
