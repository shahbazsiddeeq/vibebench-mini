import pytest
from src.solution import b64_decode, b64_encode


def test_encode_known():
    assert b64_encode(b"hello") == "aGVsbG8="


def test_decode_known():
    assert b64_decode("aGVsbG8=") == b"hello"


def test_roundtrip():
    data = b"binary\x00\xff\xfe data"
    assert b64_decode(b64_encode(data)) == data


def test_empty_bytes():
    assert b64_encode(b"") == ""


def test_empty_string_decode():
    assert b64_decode("") == b""


def test_decode_invalid_raises():
    with pytest.raises(ValueError):
        b64_decode("!!invalid!!")


@pytest.mark.parametrize(
    "data,expected",
    [
        (b"Man", "TWFu"),
        (b"AB", "QUI="),
    ],
)
def test_parametrized(data, expected):
    assert b64_encode(data) == expected
