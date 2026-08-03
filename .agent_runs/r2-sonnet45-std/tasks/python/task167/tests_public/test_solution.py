import pytest

from src.solution import decode_basic_auth, encode_basic_auth


def test_decode_basic():
    assert decode_basic_auth("Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==") == (
        "Aladdin",
        "open sesame",
    )


def test_password_may_contain_colon():
    # Mutation killer: splitting on every ':' (or the last ':') mangles a
    # password that itself contains colons; must split on the FIRST only.
    header = encode_basic_auth("Aladdin", "open:sesame")
    assert header == "Basic QWxhZGRpbjpvcGVuOnNlc2FtZQ=="
    assert decode_basic_auth(header) == ("Aladdin", "open:sesame")


def test_scheme_case_insensitive():
    assert decode_basic_auth("basic QWxhZGRpbjpvcGVuOnNlc2FtZQ==") == (
        "Aladdin",
        "open:sesame",
    )
    assert decode_basic_auth("BASIC QWxhZGRpbjpvcGVuOnNlc2FtZQ==") == (
        "Aladdin",
        "open:sesame",
    )


def test_utf8_credentials():
    header = encode_basic_auth("naïve", "pä55")
    assert decode_basic_auth(header) == ("naïve", "pä55")


def test_missing_token_rejected():
    with pytest.raises(ValueError):
        decode_basic_auth("Basic")
    with pytest.raises(ValueError):
        decode_basic_auth("Basic ")


def test_no_colon_in_credentials_rejected():
    # base64 of 'usernameonly' (no colon).
    token = "dXNlcm5hbWVvbmx5"
    with pytest.raises(ValueError):
        decode_basic_auth("Basic " + token)


def test_return_type_is_tuple():
    result = decode_basic_auth("Basic dXNlcjpwdw==")
    assert type(result) is tuple
    assert result == ("user", "pw")
