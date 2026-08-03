import pytest

from src.solution import find_mutable_defaults


def test_worked_example():
    src = (
        "def f(a, b=[]):\n"
        "    pass\n"
        "def g(x={}):\n"
        "    pass\n"
        "def h(y=(1, 2)):\n"
        "    pass\n"
    )
    assert find_mutable_defaults(src) == [("f", 1), ("g", 3)]


def test_tuple_and_constants_do_not_count():
    src = (
        "def f(a=(1, 2), b='[]', c=None, d=0, e=True):\n"
        "    return a\n"
    )
    assert find_mutable_defaults(src) == []


def test_keyword_only_defaults_checked():
    src = "def f(*, a=[], b=1):\n    return a\n"
    assert find_mutable_defaults(src) == [("f", 1)]


def test_methods_and_nested_defs():
    src = (
        "class C:\n"
        "    def m(self, x=[]):\n"
        "        def inner(y={}):\n"
        "            return y\n"
        "        return inner\n"
    )
    assert find_mutable_defaults(src) == [("m", 2), ("inner", 3)]


def test_lambda_ignored():
    # Lambdas have no name; a mutable default there must not be reported.
    src = "g = lambda a=[]: a\n"
    assert find_mutable_defaults(src) == []


def test_no_functions():
    assert find_mutable_defaults("x = [1, 2, 3]\ny = {}\n") == []
