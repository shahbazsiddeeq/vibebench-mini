import pytest

from src.solution import compute_complexity


def test_trivial_function_is_one():
    assert compute_complexity("def f():\n    return 1\n") == [("f", 1, 1)]


def test_ternary_and_comprehension_ifs():
    # IfExp (+1) and two comprehension if-clauses (+2). Base 1 => 4.
    src = (
        "def f(xs):\n"
        "    y = 1 if xs else 2\n"
        "    return [x for x in xs if x > 0 if x < 10]\n"
    )
    assert compute_complexity(src) == [("f", 1, 4)]


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


def test_sorted_by_line_then_name():
    src = (
        "def bbb():\n"
        "    return 0\n"
        "def aaa():\n"
        "    return 0\n"
    )
    assert compute_complexity(src) == [("bbb", 1, 1), ("aaa", 3, 1)]
