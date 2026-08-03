import pytest
from src.solution import rle_decode, rle_encode


def test_encode_basic():
    assert rle_encode("aaabbc") == "3a2b1c"


def test_encode_single_chars():
    assert rle_encode("abc") == "1a1b1c"


def test_encode_long_run():
    assert rle_encode("aaaaa") == "5a"


def test_roundtrip():
    s = "aabbccdd"
    assert rle_decode(rle_encode(s)) == s


def test_encode_rejects_digits():
    with pytest.raises(ValueError):
        rle_encode("a1b")


def test_decode_invalid_trailing():
    with pytest.raises(ValueError):
        rle_decode("3ab")


def test_empty_encode():
    assert rle_encode("") == ""
