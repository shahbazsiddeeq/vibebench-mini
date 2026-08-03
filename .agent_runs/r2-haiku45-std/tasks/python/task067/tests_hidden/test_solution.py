import pytest
from src.solution import gen_token


def test_returns_string():
    assert isinstance(gen_token(), str)


def test_too_small_raises():
    with pytest.raises(ValueError):
        gen_token(7)


def test_custom_length():
    t1 = gen_token(16)
    t2 = gen_token(32)
    assert len(t2) > len(t1)


def test_no_padding():
    # base64 padding must be stripped
    assert "=" not in gen_token(16)
    assert "=" not in gen_token(10)
