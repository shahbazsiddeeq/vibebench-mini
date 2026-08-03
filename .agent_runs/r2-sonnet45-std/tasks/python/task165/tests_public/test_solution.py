import pytest

from src.solution import cidr_contains


def test_basic_outside():
    assert cidr_contains("10.0.0.0/8", "11.0.0.1") is False


def test_prefix_zero_matches_all():
    assert cidr_contains("0.0.0.0/0", "8.8.8.8") is True
    assert cidr_contains("255.255.255.255/0", "1.2.3.4") is True


def test_host_bits_ignored():
    # network part has host bits set; they must be masked off.
    assert cidr_contains("192.168.1.55/24", "192.168.1.200") is True


def test_leading_zero_octet_rejected():
    # Mutation killer: a naive int() parser accepts leading zeros.
    with pytest.raises(ValueError):
        cidr_contains("192.168.001.0/24", "192.168.1.1")
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0/24", "192.168.01.1")


def test_octet_out_of_range():
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.256/24", "192.168.1.1")
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0/24", "300.1.1.1")


def test_missing_or_extra_slash():
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0", "192.168.1.1")
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0/24/8", "192.168.1.1")


def test_non_integer_prefix():
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0/x", "192.168.1.1")
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0/2.5", "192.168.1.1")
