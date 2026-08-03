import pytest
from src.solution import fib


def test_base_zero():
    assert fib(0) == 0


def test_fib_10():
    assert fib(10) == 55


def test_fib_large():
    assert fib(50) == 12586269025


def test_fib_1000_no_recursion_error():
    # Must not hit Python's recursion limit for large n.
    result = fib(1000)
    assert result == fib(999) + fib(998)
    assert len(str(result)) == 209


@pytest.mark.parametrize(
    "n,expected",
    [
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
    ],
)
def test_parametrized(n, expected):
    assert fib(n) == expected
