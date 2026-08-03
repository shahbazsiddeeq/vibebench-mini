import pytest
from src.solution import b64_decode, b64_encode


def test_decode_known():
    assert b64_decode("aGVsbG8=") == b"hello"


def test_empty_bytes():
    assert b64_encode(b"") == ""


def test_decode_invalid_raises():
    with pytest.raises(ValueError):
        b64_decode("!!invalid!!")
