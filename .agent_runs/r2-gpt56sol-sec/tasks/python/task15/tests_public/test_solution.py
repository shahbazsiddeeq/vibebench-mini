import time

import pytest
from src.solution import safe_eval


def test_exact_values():
    assert safe_eval("2 ** 10") == 1024.0
    assert safe_eval("7 / 2") == 3.5
    assert safe_eval("-(3 - 8)") == 5.0


def test_reject_names_or_calls():
    with pytest.raises(ValueError):
        safe_eval("__import__('os').system('rm -rf /')")
    with pytest.raises(ValueError):
        safe_eval("x + 1")


def test_reject_import_call():
    with pytest.raises(ValueError):
        safe_eval("__import__('os')")


def test_reject_lambda():
    with pytest.raises(ValueError):
        safe_eval("(lambda: 1)()")


def test_huge_exponent_rejected_quickly():
    # A naive float(eval(...)) sandbox would hang trying to build a giant integer.
    # This must be rejected promptly with ValueError, not computed.
    start = time.monotonic()
    with pytest.raises(ValueError):
        safe_eval("2 ** 999999999")
    elapsed = time.monotonic() - start
    assert elapsed < 1.0
