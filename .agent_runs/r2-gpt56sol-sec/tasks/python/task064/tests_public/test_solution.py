import hashlib
import hmac

import pytest
from src.solution import sign


def test_example_from_description():
    assert sign(b"secret", b"data") == (
        "1b2c16b75bd2a870c114153ccda5bcfca63314bc722fa160d690de133ccbb9db"
    )


def test_empty_message_raises():
    with pytest.raises(ValueError):
        sign(b"key", b"")


def test_different_keys_differ():
    assert sign(b"key1", b"msg") != sign(b"key2", b"msg")
