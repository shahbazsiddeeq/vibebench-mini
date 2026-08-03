import pytest
from src.solution import rle_decode, rle_encode


def test_encode_basic():
    assert rle_encode("aaabbc") == "3a2b1c"


def test_decode_basic():
    assert rle_decode("3a2b1c") == "aaabbc"


def test_encode_single_chars():
    assert rle_encode("abc") == "1a1b1c"


def test_decode_single_chars():
    assert rle_decode("1a1b1c") == "abc"


def test_encode_long_run():
    assert rle_encode("aaaaa") == "5a"


def test_encode_count_over_nine():
    assert rle_encode("a" * 12) == "12a"
    assert rle_decode("12a") == "a" * 12


def test_roundtrip():
    s = "aabbccdd"
    assert rle_decode(rle_encode(s)) == s


def test_roundtrip_with_newline():
    s = "aa\n\n\nbb"
    encoded = rle_encode(s)
    assert encoded == "2a3\n2b"
    assert rle_decode(encoded) == s


def test_encode_rejects_digits():
    with pytest.raises(ValueError):
        rle_encode("a1b")


def test_decode_invalid_no_count():
    with pytest.raises(ValueError):
        rle_decode("abc")


def test_decode_invalid_trailing():
    with pytest.raises(ValueError):
        rle_decode("3ab")


def test_decode_zero_count():
    with pytest.raises(ValueError):
        rle_decode("0a")


def test_empty_encode():
    assert rle_encode("") == ""


def test_empty_decode():
    assert rle_decode("") == ""
