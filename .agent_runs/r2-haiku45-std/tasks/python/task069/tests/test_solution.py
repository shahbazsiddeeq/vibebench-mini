import pytest
from src.solution import decode_jwt_header


def test_real_header():
    # {"alg": "HS256", "typ": "JWT"} base64url encoded
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload.sig"
    result = decode_jwt_header(token)
    assert result["alg"] == "HS256"


def test_no_dot_raises():
    with pytest.raises(ValueError):
        decode_jwt_header("nodottoken")


def test_invalid_base64_raises():
    with pytest.raises(ValueError):
        decode_jwt_header("!!!.payload.sig")


def test_not_json_raises():
    import base64

    bad = base64.urlsafe_b64encode(b"not-json").decode()
    with pytest.raises(ValueError):
        decode_jwt_header(f"{bad}.p.s")


def test_returns_dict():
    token = "eyJhbGciOiJIUzI1NiJ9.payload.sig"
    assert isinstance(decode_jwt_header(token), dict)


def test_unpadded_segment():
    import base64
    import json

    header = {"alg": "HS256", "typ": "JWT", "kid": "a1"}
    raw = (
        base64.urlsafe_b64encode(json.dumps(header, separators=(",", ":")).encode())
        .rstrip(b"=")
        .decode()
    )
    # ensure the segment actually needs padding re-added (length not a multiple of 4)
    assert len(raw) % 4 != 0
    assert decode_jwt_header(f"{raw}.payload.sig") == header


def test_non_object_header_raises():
    import base64
    import json

    for value in ([1, 2, 3], 42, "just-a-string"):
        raw = (
            base64.urlsafe_b64encode(json.dumps(value).encode())
            .rstrip(b"=")
            .decode()
        )
        with pytest.raises(ValueError):
            decode_jwt_header(f"{raw}.p.s")
