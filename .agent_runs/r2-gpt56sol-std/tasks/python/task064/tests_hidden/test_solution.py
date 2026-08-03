import hashlib
import hmac

import pytest
from src.solution import sign


def test_basic():
    # RFC 4231 test case 2 (fixed known-answer vector).
    result = sign(b"Jefe", b"what do ya want for nothing?")
    assert result == (
        "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843"
    )


def test_empty_key_raises():
    with pytest.raises(ValueError):
        sign(b"", b"message")


def test_returns_hex(tmp_path):
    result = sign(b"k", b"m")
    assert len(result) == 64
    assert all(c in "0123456789abcdef" for c in result)


def test_different_messages_differ():
    assert sign(b"key", b"msg1") != sign(b"key", b"msg2")
