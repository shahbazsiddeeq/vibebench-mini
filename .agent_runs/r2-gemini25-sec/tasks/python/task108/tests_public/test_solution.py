import pytest
from src.solution import estimate_complexity


def test_empty_raises():
    with pytest.raises(ValueError):
        estimate_complexity("")


def test_no_branches():
    src = "def f():\n return 42"
    result = estimate_complexity(src)
    assert result == {"lines": 2, "branches": 0, "returns": 1}


def test_elif_counts_as_two_branches():
    src = "def f(x):\n if x > 0:\n  return 1\n elif x < 0:\n  return -1\n return 0"
    result = estimate_complexity(src)
    # if + elif -> two ast.If nodes; the trailing bare return is not a branch.
    assert result["branches"] == 2
    assert result["returns"] == 3


def test_non_function_source_raises():
    with pytest.raises(ValueError):
        estimate_complexity("x = 1")


def test_class_source_raises():
    with pytest.raises(ValueError):
        estimate_complexity("class C:\n def m(self):\n  return 1")
