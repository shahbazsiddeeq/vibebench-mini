import pytest
from src.solution import gen_token


def test_returns_string():
    assert isinstance(gen_token(), str)


def test_unique():
    assert gen_token() != gen_token()


def test_too_small_raises():
    with pytest.raises(ValueError):
        gen_token(7)


def test_boundary_ok():
    t = gen_token(8)
    assert len(t) > 0


def test_custom_length():
    t1 = gen_token(16)
    t2 = gen_token(32)
    assert len(t2) > len(t1)


def test_url_safe_chars():
    import re

    t = gen_token(32)
    assert re.match(r"^[A-Za-z0-9_-]+$", t)


def test_no_padding():
    # base64 padding must be stripped
    assert "=" not in gen_token(16)
    assert "=" not in gen_token(10)


def test_exact_length():
    # exact unpadded base64url length = (4*n + 2) // 3
    for n in (8, 10, 16, 32, 48):
        assert len(gen_token(n)) == (4 * n + 2) // 3
