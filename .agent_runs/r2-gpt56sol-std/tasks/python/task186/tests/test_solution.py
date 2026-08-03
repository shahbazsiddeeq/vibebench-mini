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


def test_trivial_function_is_one():
    assert compute_complexity("def f():\n    return 1\n") == [("f", 1, 1)]


def test_boolop_multiple_operands():
    # a and b and c -> BoolOp with 3 values -> +2. Base 1 => 3.
    src = "def f(a, b, c):\n    return a and b and c\n"
    assert compute_complexity(src) == [("f", 1, 3)]


def test_ternary_and_comprehension_ifs():
    # IfExp (+1) and two comprehension if-clauses (+2). Base 1 => 4.
    src = (
        "def f(xs):\n"
        "    y = 1 if xs else 2\n"
        "    return [x for x in xs if x > 0 if x < 10]\n"
    )
    assert compute_complexity(src) == [("f", 1, 4)]


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


def test_nested_function_measured_separately():
    src = (
        "def outer(x):\n"
        "    if x:\n"
        "        pass\n"
        "    def inner(y):\n"
        "        if y and x:\n"
        "            return 1\n"
        "        return 0\n"
        "    return inner\n"
    )
    # outer: base 1 + if = 2 (inner's body excluded)
    # inner: base 1 + if + and = 3
    assert compute_complexity(src) == [("outer", 1, 2), ("inner", 4, 3)]


def test_methods_reported_and_lambda_ignored():
    src = (
        "class C:\n"
        "    def m(self, a):\n"
        "        return 1 if a else 2\n"
        "    g = lambda z: z or 0\n"
    )
    assert compute_complexity(src) == [("m", 2, 2)]


def test_mutation_killer_keywords_in_strings_and_comments():
    # A regex/line scanner counting the words if/for/while/and/except in the
    # text would inflate complexity. Only real control flow counts here.
    src = (
        "def f(a):\n"
        "    s = 'if for while and or except elif'\n"
        "    # if for while and except\n"
        "    return len(s)\n"
    )
    assert compute_complexity(src) == [("f", 1, 1)]


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


def test_sorted_by_line_then_name():
    src = (
        "def bbb():\n"
        "    return 0\n"
        "def aaa():\n"
        "    return 0\n"
    )
    assert compute_complexity(src) == [("bbb", 1, 1), ("aaa", 3, 1)]


def test_invalid_source_raises():
    with pytest.raises(ValueError):
        compute_complexity("def f(:\n")
