import pytest
from src.solution import rle_decode, rle_encode


def test_decode_basic():
    assert rle_decode("3a2b1c") == "aaabbc"


def test_decode_single_chars():
    assert rle_decode("1a1b1c") == "abc"


def test_encode_count_over_nine():
    assert rle_encode("a" * 12) == "12a"
    assert rle_decode("12a") == "a" * 12


def test_roundtrip_with_newline():
    s = "aa\n\n\nbb"
    encoded = rle_encode(s)
    assert encoded == "2a3\n2b"
    assert rle_decode(encoded) == s


def test_decode_invalid_no_count():
    with pytest.raises(ValueError):
        rle_decode("abc")


def test_decode_zero_count():
    with pytest.raises(ValueError):
        rle_decode("0a")


def test_empty_decode():
    assert rle_decode("") == ""
