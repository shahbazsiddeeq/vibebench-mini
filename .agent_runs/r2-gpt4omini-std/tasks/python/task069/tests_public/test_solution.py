import pytest
from src.solution import decode_jwt_header


def test_no_dot_raises():
    with pytest.raises(ValueError):
        decode_jwt_header("nodottoken")


def test_not_json_raises():
    import base64

    bad = base64.urlsafe_b64encode(b"not-json").decode()
    with pytest.raises(ValueError):
        decode_jwt_header(f"{bad}.p.s")


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
