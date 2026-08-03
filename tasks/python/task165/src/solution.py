import re

_OCTET = re.compile(r"[0-9]+")


def _parse_octet(part: str) -> int:
    if not _OCTET.fullmatch(part):
        raise ValueError(f"invalid octet: {part!r}")
    if len(part) > 1 and part[0] == "0":
        raise ValueError(f"octet has leading zero: {part!r}")
    value = int(part)
    if value > 255:
        raise ValueError(f"octet out of range: {part!r}")
    return value


def _parse_ipv4(ip: str) -> int:
    if not isinstance(ip, str):
        raise ValueError("ip must be a string")
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError(f"IPv4 address must have 4 octets: {ip!r}")
    result = 0
    for part in parts:
        result = (result << 8) | _parse_octet(part)
    return result


def _parse_prefix(prefix: str) -> int:
    if not _OCTET.fullmatch(prefix):
        raise ValueError(f"invalid prefix: {prefix!r}")
    if len(prefix) > 1 and prefix[0] == "0":
        raise ValueError(f"prefix has leading zero: {prefix!r}")
    value = int(prefix)
    if value > 32:
        raise ValueError(f"prefix out of range: {prefix!r}")
    return value


def cidr_contains(cidr: str, ip: str) -> bool:
    """Return True iff IPv4 ``ip`` lies inside IPv4 ``cidr`` block.

    Strict parsing: dotted-decimal octets 0-255 with no leading zeros;
    prefix length is an integer 0-32 with no leading zeros. Host bits of
    the CIDR are ignored for the membership test. Raises ValueError on any
    malformed input.
    """
    if not isinstance(cidr, str):
        raise ValueError("cidr must be a string")
    parts = cidr.split("/")
    if len(parts) != 2:
        raise ValueError(f"CIDR must be network/prefix: {cidr!r}")
    net_str, prefix_str = parts
    network = _parse_ipv4(net_str)
    prefix = _parse_prefix(prefix_str)
    address = _parse_ipv4(ip)
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return (address & mask) == (network & mask)
