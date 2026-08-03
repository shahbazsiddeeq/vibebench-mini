import re

_OCTET_RE = re.compile(r'^(0|[1-9][0-9]{0,2})$')


def _parse_ip(ip: str) -> int:
    if not isinstance(ip, str):
        raise ValueError("IP must be a string")
    parts = ip.split('.')
    if len(parts) != 4:
        raise ValueError(f"Invalid IP address: {ip!r}")
    value = 0
    for part in parts:
        if not _OCTET_RE.match(part):
            raise ValueError(f"Invalid octet: {part!r} in {ip!r}")
        num = int(part)
        if num < 0 or num > 255:
            raise ValueError(f"Octet out of range: {part!r} in {ip!r}")
        value = (value << 8) | num
    return value


def _parse_prefix(prefix_str: str) -> int:
    if not _OCTET_RE.match(prefix_str):
        raise ValueError(f"Invalid prefix: {prefix_str!r}")
    prefix = int(prefix_str)
    if prefix < 0 or prefix > 32:
        raise ValueError(f"Prefix out of range: {prefix_str!r}")
    return prefix


def cidr_contains(cidr: str, ip: str) -> bool:
    if not isinstance(cidr, str):
        raise ValueError("CIDR must be a string")
    if cidr.count('/') != 1:
        raise ValueError(f"Invalid CIDR (must contain exactly one '/'): {cidr!r}")

    net_str, prefix_str = cidr.split('/')
    network_int = _parse_ip(net_str)
    prefix = _parse_prefix(prefix_str)
    ip_int = _parse_ip(ip)

    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

    return (ip_int & mask) == (network_int & mask)
