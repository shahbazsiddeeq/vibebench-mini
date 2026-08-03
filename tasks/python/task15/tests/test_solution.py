import time

import pytest
from src.solution import safe_eval


def test_basic_ops():
    assert safe_eval("1 + 2*3") == 7.0
    assert safe_eval("(2+3)**2") == 25.0
    assert safe_eval("-4 + +1") == -3.0


def test_exact_values():
    assert safe_eval("2 ** 10") == 1024.0
    assert safe_eval("7 / 2") == 3.5
    assert safe_eval("-(3 - 8)") == 5.0


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        safe_eval("1/0")


def test_reject_names_or_calls():
    with pytest.raises(ValueError):
        safe_eval("__import__('os').system('rm -rf /')")
    with pytest.raises(ValueError):
        safe_eval("x + 1")


def test_reject_attribute_and_dunder_traversal():
    # The classic sandbox-escape gadget: reach object subclasses via dunders.
    with pytest.raises(ValueError):
        safe_eval("().__class__.__mro__[1].__subclasses__()")
    with pytest.raises(ValueError):
        safe_eval("(1).__class__")


def test_reject_import_call():
    with pytest.raises(ValueError):
        safe_eval("__import__('os')")


def test_reject_comprehension():
    with pytest.raises(ValueError):
        safe_eval("[x for x in range(10)]")


def test_reject_lambda():
    with pytest.raises(ValueError):
        safe_eval("(lambda: 1)()")


def test_reject_boolean_literal():
    with pytest.raises(ValueError):
        safe_eval("True")


def test_huge_exponent_rejected_quickly():
    # A naive float(eval(...)) sandbox would hang trying to build a giant integer.
    # This must be rejected promptly with ValueError, not computed.
    start = time.monotonic()
    with pytest.raises(ValueError):
        safe_eval("2 ** 999999999")
    elapsed = time.monotonic() - start
    assert elapsed < 1.0
