import pytest
from src.solution import fib


def test_base_one():
    assert fib(1) == 1


def test_fib_20():
    assert fib(20) == 6765


def test_negative_raises():
    with pytest.raises(ValueError):
        fib(-1)


def test_memo_persists_across_calls():
    # Second call for an already-computed n must return the same value.
    first = fib(90)
    assert fib(90) == first == 2880067194370816120
