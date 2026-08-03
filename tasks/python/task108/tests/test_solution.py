import pytest
from src.solution import estimate_complexity


def test_basic():
    src = "def f(x):\n if x: return 1\n return 0"
    result = estimate_complexity(src)
    assert result == {"lines": 3, "branches": 1, "returns": 2}


def test_empty_raises():
    with pytest.raises(ValueError):
        estimate_complexity("")


def test_invalid_syntax():
    with pytest.raises(ValueError):
        estimate_complexity("def f(: pass")


def test_no_branches():
    src = "def f():\n return 42"
    result = estimate_complexity(src)
    assert result == {"lines": 2, "branches": 0, "returns": 1}


def test_for_loop_counts_as_branch():
    src = "def f(lst):\n for x in lst:\n  pass\n return lst"
    result = estimate_complexity(src)
    assert result["branches"] == 1
    assert result["returns"] == 1


def test_elif_counts_as_two_branches():
    src = "def f(x):\n if x > 0:\n  return 1\n elif x < 0:\n  return -1\n return 0"
    result = estimate_complexity(src)
    # if + elif -> two ast.If nodes; the trailing bare return is not a branch.
    assert result["branches"] == 2
    assert result["returns"] == 3


def test_while_and_except_count():
    src = (
        "def f(n):\n"
        " while n > 0:\n"
        "  try:\n"
        "   n -= 1\n"
        "  except ValueError:\n"
        "   pass\n"
        " return n"
    )
    result = estimate_complexity(src)
    # while (1) + except handler (1); the try header itself does not count.
    assert result["branches"] == 2
    assert result["returns"] == 1


def test_non_function_source_raises():
    with pytest.raises(ValueError):
        estimate_complexity("x = 1")


def test_multiple_top_level_defs_raise():
    with pytest.raises(ValueError):
        estimate_complexity("def f():\n return 1\ndef g():\n return 2")


def test_class_source_raises():
    with pytest.raises(ValueError):
        estimate_complexity("class C:\n def m(self):\n  return 1")
