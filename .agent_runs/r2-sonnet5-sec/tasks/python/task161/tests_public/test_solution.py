import pytest

from src.solution import totp

# RFC 6238 Appendix B SHA-1 test vectors (seed = ASCII "12345678901234567890"),
# 8-digit codes, 30-second period. Hardcoded published literals.
SEED = b"12345678901234567890"
RFC_VECTORS = {
    59: "94287082",
    1111111109: "07081804",
    1111111111: "14050471",
    1234567890: "89005924",
    2000000000: "69279037",
    20000000000: "65353130",
}


def test_returns_string_zero_padded():
    code = totp(SEED, 59, period=30, digits=8)
    assert isinstance(code, str)
    assert len(code) == 8


def test_same_window_same_code():
    # timestamps 30..59 fall in counter=1 (period 30, t0 0).
    assert totp(SEED, 30, period=30, digits=8) == totp(SEED, 59, period=30, digits=8)


def test_t0_offset_shifts_window():
    # With t0=30, timestamp 89 maps to counter=1, matching the plain counter=1 code.
    assert totp(SEED, 89, period=30, digits=8, t0=30) == RFC_VECTORS[59]


def test_type_errors():
    with pytest.raises(TypeError):
        totp("notbytes", 59)
    with pytest.raises(TypeError):
        totp(SEED, True)
