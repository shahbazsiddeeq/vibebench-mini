import pytest
from src.solution import xor_cipher


def test_encrypt_basic():
    result = xor_cipher(b"\x00", b"\xff")
    assert result == b"\xff"


def test_empty_key_raises():
    with pytest.raises(ValueError):
        xor_cipher(b"data", b"")


def test_multibyte_key_exact_vector():
    # Two-byte key must alternate a,b,a,b,a across the 5 bytes.
    assert xor_cipher(b"hello", b"ab") == b"\x09\x07\x0d\x0e\x0e"


def test_different_keys_differ():
    assert xor_cipher(b"hello", b"k1") != xor_cipher(b"hello", b"k2")
