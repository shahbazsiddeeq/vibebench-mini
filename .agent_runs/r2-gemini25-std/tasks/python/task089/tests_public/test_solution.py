from unittest.mock import patch

import pytest
from src.solution import retry


def test_fails_then_succeeds():
    calls = [0]

    def fn():
        calls[0] += 1
        if calls[0] < 3:
            raise IOError("fail")
        return "ok"

    with patch("time.sleep"):
        result = retry(fn, 3, 0.01, (IOError,))
    assert result == "ok"


def test_wrong_exception_propagates():
    def fn():
        raise TypeError("not in exceptions tuple")

    with pytest.raises(TypeError):
        retry(fn, 3, 0.0, (ValueError,))


def test_backoff_sleep_sequence():
    def fn():
        raise IOError("fail")

    with patch("time.sleep") as mock_sleep:
        with pytest.raises(IOError):
            retry(fn, 4, 1.0, (IOError,))
    delays = [c.args[0] for c in mock_sleep.call_args_list]
    # base_delay * 2**attempt for attempts 0..2; no sleep after the last attempt
    assert delays == [1.0, 2.0, 4.0]


def test_raises_last_exception_not_first():
    calls = [0]

    def fn():
        calls[0] += 1
        raise ValueError(f"attempt {calls[0]}")

    with patch("time.sleep"):
        with pytest.raises(ValueError) as excinfo:
            retry(fn, 3, 0.01, (ValueError,))
    assert "attempt 3" in str(excinfo.value)
