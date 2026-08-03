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


@pytest.mark.parametrize("ts,expected", list(RFC_VECTORS.items()))
def test_rfc6238_sha1_vectors(ts, expected):
    assert totp(SEED, ts, period=30, digits=8, algorithm="sha1") == expected


def test_default_digits_is_6():
    code = totp(SEED, 59)
    assert len(code) == 6
    # First 6 digits are the low-order digits of the 8-digit vector.
    assert code == "287082"


def test_next_window_differs():
    assert totp(SEED, 59, period=30, digits=8) != totp(SEED, 60, period=30, digits=8)


def test_mutation_period_matters():
    assert totp(SEED, 59, period=30, digits=8) != totp(SEED, 59, period=60, digits=8)


def test_value_errors():
    with pytest.raises(ValueError):
        totp(SEED, 59, period=0)
    with pytest.raises(ValueError):
        totp(SEED, 59, digits=0)
    with pytest.raises(ValueError):
        totp(SEED, 59, digits=11)
    with pytest.raises(ValueError):
        totp(SEED, 59, algorithm="md5")
    with pytest.raises(ValueError):
        totp(SEED, 10, t0=30)
