import time

import pytest
from src.solution import safe_eval


def test_basic_ops():
    assert safe_eval("1 + 2*3") == 7.0
    assert safe_eval("(2+3)**2") == 25.0
    assert safe_eval("-4 + +1") == -3.0


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        safe_eval("1/0")


def test_reject_attribute_and_dunder_traversal():
    # The classic sandbox-escape gadget: reach object subclasses via dunders.
    with pytest.raises(ValueError):
        safe_eval("().__class__.__mro__[1].__subclasses__()")
    with pytest.raises(ValueError):
        safe_eval("(1).__class__")


def test_reject_comprehension():
    with pytest.raises(ValueError):
        safe_eval("[x for x in range(10)]")


def test_reject_boolean_literal():
    with pytest.raises(ValueError):
        safe_eval("True")
