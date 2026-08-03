import pytest

from src.solution import cidr_contains


def test_basic_inside():
    assert cidr_contains("192.168.1.0/24", "192.168.1.42") is True


def test_boundary_addresses():
    assert cidr_contains("10.0.0.0/8", "10.0.0.0") is True
    assert cidr_contains("10.0.0.0/8", "10.255.255.255") is True
    assert cidr_contains("10.0.0.0/8", "9.255.255.255") is False


def test_prefix_32_exact_match():
    assert cidr_contains("192.168.0.1/32", "192.168.0.1") is True
    assert cidr_contains("192.168.0.1/32", "192.168.0.2") is False


def test_non_octet_aligned_prefix():
    # /26 -> mask 255.255.255.192
    assert cidr_contains("192.168.1.0/26", "192.168.1.63") is True
    assert cidr_contains("192.168.1.0/26", "192.168.1.64") is False


def test_leading_zero_prefix_rejected():
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0/024", "192.168.1.1")


def test_prefix_out_of_range():
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0/33", "192.168.1.1")


def test_wrong_octet_count():
    with pytest.raises(ValueError):
        cidr_contains("192.168.1/24", "192.168.1.1")
    with pytest.raises(ValueError):
        cidr_contains("192.168.1.0/24", "192.168.1.1.1")


def test_return_type_is_bool():
    assert type(cidr_contains("1.2.3.4/32", "1.2.3.4")) is bool
