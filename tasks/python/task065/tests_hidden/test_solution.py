import pytest
from src.solution import b64_decode, b64_encode


def test_encode_known():
    assert b64_encode(b"hello") == "aGVsbG8="


def test_roundtrip():
    data = b"binary\x00\xff\xfe data"
    assert b64_decode(b64_encode(data)) == data


def test_empty_string_decode():
    assert b64_decode("") == b""


@pytest.mark.parametrize(
    "data,expected",
    [
        (b"Man", "TWFu"),
        (b"AB", "QUI="),
    ],
)
def test_parametrized(data, expected):
    assert b64_encode(data) == expected
