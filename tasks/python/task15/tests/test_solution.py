import pytest
from src.solution import safe_eval


def test_basic_ops():
    assert safe_eval("1 + 2*3") == 7.0
    assert safe_eval("(2+3)**2") == 25.0
    assert safe_eval("-4 + +1") == -3.0


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        safe_eval("1/0")


def test_reject_names_or_calls():
    with pytest.raises(ValueError):
        safe_eval("__import__('os').system('rm -rf /')")
    with pytest.raises(ValueError):
        safe_eval("x + 1")
