import pytest

from src.solution import compute_complexity


def test_worked_example():
    src = (
        "def f(a):\n"
        "    if a > 0:\n"
        "        for i in range(a):\n"
        "            if i % 2 == 0 and i > 1:\n"
        "                print(i)\n"
        "    return a\n"
    )
    assert compute_complexity(src) == [("f", 1, 5)]


def test_boolop_multiple_operands():
    # a and b and c -> BoolOp with 3 values -> +2. Base 1 => 3.
    src = "def f(a, b, c):\n    return a and b and c\n"
    assert compute_complexity(src) == [("f", 1, 3)]


def test_except_handlers_count_but_try_does_not():
    src = (
        "def f():\n"
        "    try:\n"
        "        g()\n"
        "    except ValueError:\n"
        "        pass\n"
        "    except KeyError:\n"
        "        pass\n"
    )
    # base 1 + 2 except handlers = 3
    assert compute_complexity(src) == [("f", 1, 3)]


def test_methods_reported_and_lambda_ignored():
    src = (
        "class C:\n"
        "    def m(self, a):\n"
        "        return 1 if a else 2\n"
        "    g = lambda z: z or 0\n"
    )
    assert compute_complexity(src) == [("m", 2, 2)]


def test_elif_each_counts():
    src = (
        "def f(a):\n"
        "    if a == 1:\n"
        "        return 1\n"
        "    elif a == 2:\n"
        "        return 2\n"
        "    elif a == 3:\n"
        "        return 3\n"
        "    else:\n"
        "        return 0\n"
    )
    # base 1 + if + elif + elif = 4 (else adds nothing)
    assert compute_complexity(src) == [("f", 1, 4)]


def test_invalid_source_raises():
    with pytest.raises(ValueError):
        compute_complexity("def f(:\n")
