import pytest

from src.solution import find_untyped_functions


def test_worked_example():
    src = (
        "def add(a, b):\n"
        "    return a + b\n"
        "def mul(a: int, b: int) -> int:\n"
        "    return a * b\n"
    )
    assert find_untyped_functions(src) == [("add", 1)]


def test_missing_return_annotation_only():
    src = "def f(a: int, b: int):\n    return a + b\n"
    assert find_untyped_functions(src) == [("f", 1)]


def test_self_and_cls_exempt_in_methods():
    src = (
        "class C:\n"
        "    def m(self, x: int) -> int:\n"
        "        return x\n"
        "    @classmethod\n"
        "    def k(cls) -> int:\n"
        "        return 1\n"
        "    def __init__(self) -> None:\n"
        "        pass\n"
    )
    assert find_untyped_functions(src) == []


def test_method_with_unannotated_second_param():
    src = (
        "class C:\n"
        "    def n(self, y) -> int:\n"
        "        return y\n"
    )
    assert find_untyped_functions(src) == [("n", 2)]


def test_self_not_exempt_at_module_level():
    # A module-level function named with a self parameter is not a method.
    src = "def free(self) -> int:\n    return 1\n"
    assert find_untyped_functions(src) == [("free", 1)]


def test_self_not_exempt_in_nested_function():
    src = (
        "class C:\n"
        "    def m(self) -> int:\n"
        "        def inner(self) -> int:\n"
        "            return 1\n"
        "        return inner(self)\n"
    )
    assert find_untyped_functions(src) == [("inner", 3)]


def test_varargs_and_kwargs_require_annotation():
    src = "def f(*args, **kwargs) -> None:\n    pass\n"
    assert find_untyped_functions(src) == [("f", 1)]


def test_fully_annotated_varargs_ok():
    src = "def f(*args: int, **kwargs: str) -> None:\n    pass\n"
    assert find_untyped_functions(src) == []


def test_defaults_still_need_annotations():
    src = "def f(a=1, b: int = 2) -> int:\n    return a + b\n"
    assert find_untyped_functions(src) == [("f", 1)]


def test_reported_once_and_sorted():
    src = (
        "def zzz(a, b):\n"
        "    return 0\n"
        "def aaa(a):\n"
        "    return 0\n"
    )
    assert find_untyped_functions(src) == [("zzz", 1), ("aaa", 3)]


def test_mutation_killer_annotations_in_strings():
    # A regex scanner keying on ':' or '->' in the text could be fooled by the
    # arrow / colon inside the string; the function itself is fully annotated.
    src = (
        "def f(a: int) -> int:\n"
        "    s = 'def g(x) -> y: no annotations here'\n"
        "    return a\n"
    )
    assert find_untyped_functions(src) == []


def test_invalid_source_raises():
    with pytest.raises(ValueError):
        find_untyped_functions("def f(:\n")
