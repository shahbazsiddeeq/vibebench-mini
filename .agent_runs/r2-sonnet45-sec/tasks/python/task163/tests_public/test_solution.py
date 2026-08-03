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
def test_decode_vectors(raw, enc):
    assert base32_decode(enc) == raw


def test_decode_is_case_insensitive():
    assert base32_decode("mzxw6ytboi======") == b"foobar"


def test_mutation_padding_matters():
    # A correct encoder must produce exactly this padding, not e.g. "MZXW6" unpadded.
    assert base32_encode(b"foo") == "MZXW6==="
    assert base32_encode(b"foo") != "MZXW6"


def test_encode_type_error():
    with pytest.raises(TypeError):
        base32_encode("foo")


def test_decode_bad_length():
    with pytest.raises(ValueError):
        base32_decode("MZXW6")


def test_decode_misplaced_padding():
    with pytest.raises(ValueError):
        base32_decode("M=XW6YTB")
