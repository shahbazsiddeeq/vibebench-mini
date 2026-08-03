import pytest

from src.solution import decode_basic_auth, encode_basic_auth


def test_encode_basic():
    assert encode_basic_auth("Aladdin", "open sesame") == (
        "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
    )


def test_roundtrip():
    header = encode_basic_auth("user", "p@ss:word/with:colons")
    assert decode_basic_auth(header) == ("user", "p@ss:word/with:colons")


def test_username_with_colon_rejected_on_encode():
    with pytest.raises(ValueError):
        encode_basic_auth("bad:user", "pw")


def test_empty_password():
    header = encode_basic_auth("user", "")
    assert decode_basic_auth(header) == ("user", "")


def test_wrong_scheme_rejected():
    with pytest.raises(ValueError):
        decode_basic_auth("Bearer QWxhZGRpbjpvcGVu")


def test_invalid_base64_rejected():
    with pytest.raises(ValueError):
        decode_basic_auth("Basic not_base64!!")


def test_invalid_utf8_rejected():
    import base64 as _b64

    token = _b64.b64encode(b"\xff\xfe:pw").decode("ascii")
    with pytest.raises(ValueError):
        decode_basic_auth("Basic " + token)
