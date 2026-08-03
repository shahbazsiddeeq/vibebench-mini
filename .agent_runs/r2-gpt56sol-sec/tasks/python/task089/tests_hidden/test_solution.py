from unittest.mock import patch

import pytest
from src.solution import retry


def test_succeeds_first_try():
    calls = [0]

    def fn():
        calls[0] += 1
        return 42

    assert retry(fn, 3, 0.0, (Exception,)) == 42
    assert calls[0] == 1


def test_all_fail_raises():
    def fn():
        raise ValueError("always fails")

    with patch("time.sleep"), pytest.raises(ValueError):
        retry(fn, 3, 0.01, (ValueError,))


def test_max_attempts_zero_raises():
    with pytest.raises(ValueError):
        retry(lambda: None, 0, 0.0, (Exception,))


def test_calls_func_max_attempts_times():
    calls = [0]

    def fn():
        calls[0] += 1
        raise IOError("fail")

    with patch("time.sleep"):
        with pytest.raises(IOError):
            retry(fn, 3, 0.5, (IOError,))
    assert calls[0] == 3
