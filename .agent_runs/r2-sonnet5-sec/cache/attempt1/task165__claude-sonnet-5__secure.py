"""
IPv4 CIDR membership checking utility.

This module provides a strict, security-conscious parser for IPv4 dotted
addresses and CIDR blocks, and a function to test whether a given IPv4
address falls within a given CIDR block.

Design notes:
 - No use of eval/exec or any dynamic code execution.
 - No external network or file I/O.
 - Strict input validation: rejects leading zeros, out-of-range octets,
   malformed prefixes, and malformed structure.
 - Errors are surfaced only as ValueError with a generic, non-sensitive
   message (no internal state or stack details are exposed).
"""

from __future__ import annotations

_OCTET_COUNT = 4
_MAX_OCTET = 255
_MAX_PREFIX = 32


def _is_strict_nonnegative_int_str(s: str) -> bool:
    """Return True if s is a valid non-negative integer string with no
    leading zeros (except the single '0' itself), and contains only digits.
    """
    if not isinstance(s, str) or len(s) == 0:
        return False
    if not s.isdigit():
        return False
    if len(s) > 1 and s[0] == "0":
        return False
    return True


def _parse_ipv4(ip: str) -> int:
    """Strictly parse an IPv4 dotted-decimal string into a 32-bit integer.

    Raises ValueError on any malformed input.
    """
    if not isinstance(ip, str):
        raise ValueError("Invalid IPv4 address")

    parts = ip.split(".")
    if len(parts) != _OCTET_COUNT:
        raise ValueError("Invalid IPv4 address")

    value = 0
    for part in parts:
        if not _is_strict_nonnegative_int_str(part):
            raise ValueError("Invalid IPv4 address")
        octet = int(part)
        if octet < 0 or octet > _MAX_OCTET:
            raise ValueError("Invalid IPv4 address")
        value = (value << 8) | octet

    return value


def _parse_prefix(prefix_str: str) -> int:
    """Strictly parse a CIDR prefix length string into an int 0-32."""
    if not _is_strict_nonnegative_int_str(prefix_str):
        raise ValueError("Invalid CIDR prefix")
    prefix = int(prefix_str)
    if prefix < 0 or prefix > _MAX_PREFIX:
        raise ValueError("Invalid CIDR prefix")
    return prefix


def _parse_cidr(cidr: str) -> tuple[int, int]:
    """Strictly parse a CIDR string 'a.b.c.d/n' into (network_int, prefix)."""
    if not isinstance(cidr, str):
        raise ValueError("Invalid CIDR block")

    parts = cidr.split("/")
    if len(parts) != 2:
        raise ValueError("Invalid CIDR block")

    network_str, prefix_str = parts
    network_int = _parse_ipv4(network_str)
    prefix = _parse_prefix(prefix_str)

    return network_int, prefix


def cidr_contains(cidr: str, ip: str) -> bool:
    """Return True iff the IPv4 address `ip` lies within the IPv4 block
    `cidr` (network/prefix notation).

    Raises ValueError on any malformed cidr or ip input.
    """
    network_int, prefix = _parse_cidr(cidr)
    ip_int = _parse_ipv4(ip)

    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF if prefix > 0 else 0

    return (ip_int & mask) == (network_int & mask)
