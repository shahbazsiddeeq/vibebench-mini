import pytest
from src.solution import xor_cipher


def test_roundtrip():
    data = b"hello world"
    key = b"key"
    assert xor_cipher(xor_cipher(data, key), key) == data


def test_empty_data():
    assert xor_cipher(b"", b"key") == b""


def test_key_cycles():
    data = b"ab"
    key = b"k"
    result = xor_cipher(data, key)
    assert result[0] == data[0] ^ key[0]
    assert result[1] == data[1] ^ key[0]


def test_multibyte_key_roundtrip():
    data = b"attack at dawn"
    key = b"XYZ1"
    assert xor_cipher(xor_cipher(data, key), key) == data
