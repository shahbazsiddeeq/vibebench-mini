import pytest

from src.solution import base32_encode, base32_decode

# RFC 4648 Section 10 test vectors, hardcoded literals.
VECTORS = {
    b"": "",
    b"f": "MY======",
    b"fo": "MZXQ====",
    b"foo": "MZXW6===",
    b"foob": "MZXW6YQ=",
    b"fooba": "MZXW6YTB",
    b"foobar": "MZXW6YTBOI======",
}


@pytest.mark.parametrize("raw,enc", list(VECTORS.items()))
def test_encode_vectors(raw, enc):
    assert base32_encode(raw) == enc


@pytest.mark.parametrize("raw,enc", list(VECTORS.items()))
def test_decode_vectors(raw, enc):
    assert base32_decode(enc) == raw


@pytest.mark.parametrize("raw", list(VECTORS.keys()))
def test_roundtrip_bytes(raw):
    assert base32_decode(base32_encode(raw)) == raw


def test_decode_is_case_insensitive():
    assert base32_decode("mzxw6ytboi======") == b"foobar"


def test_encode_length_multiple_of_8():
    for raw in VECTORS:
        assert len(base32_encode(raw)) % 8 == 0


def test_mutation_padding_matters():
    # A correct encoder must produce exactly this padding, not e.g. "MZXW6" unpadded.
    assert base32_encode(b"foo") == "MZXW6==="
    assert base32_encode(b"foo") != "MZXW6"


def test_full_byte_range_roundtrip():
    raw = bytes(range(256))
    assert base32_decode(base32_encode(raw)) == raw


def test_encode_type_error():
    with pytest.raises(TypeError):
        base32_encode("foo")


def test_decode_type_error():
    with pytest.raises(TypeError):
        base32_decode(b"MZXW6===")


def test_decode_bad_length():
    with pytest.raises(ValueError):
        base32_decode("MZXW6")


def test_decode_invalid_char():
    with pytest.raises(ValueError):
        base32_decode("MZXW6Y18")  # '1' and '8' are not in the alphabet


def test_decode_misplaced_padding():
    with pytest.raises(ValueError):
        base32_decode("M=XW6YTB")


def test_decode_invalid_pad_count():
    # "MZXW6===" (3 pad) is the valid encoding of b"foo"; an illegal pad count is 2, 5 or 7.
    assert base32_decode("MZXW6===") == b"foo"
    with pytest.raises(ValueError):
        base32_decode("MZXW6Y==")  # 6 data + 2 pad -> pad count 2 is not one of {0,1,3,4,6}
