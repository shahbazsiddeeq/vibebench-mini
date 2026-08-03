"""Strict IPv4 CIDR membership checking."""


def _is_ascii_decimal(value: str) -> bool:
    return bool(value) and all("0" <= character <= "9" for character in value)


def _parse_ipv4(address: str) -> int:
    if not isinstance(address, str):
        raise ValueError("IPv4 address must be a string")

    octets = address.split(".")
    if len(octets) != 4:
        raise ValueError("IPv4 address must contain exactly four octets")

    result = 0
    for octet in octets:
        if not _is_ascii_decimal(octet):
            raise ValueError("IPv4 octets must be decimal integers")
        if len(octet) > 1 and octet[0] == "0":
            raise ValueError("IPv4 octets must not contain leading zeros")
        if len(octet) > 3:
            raise ValueError("IPv4 octet is out of range")

        number = int(octet)
        if number > 255:
            raise ValueError("IPv4 octet is out of range")
        result = (result << 8) | number

    return result


def _parse_prefix(prefix: str) -> int:
    if not _is_ascii_decimal(prefix):
        raise ValueError("CIDR prefix must be a decimal integer")
    if len(prefix) > 1 and prefix[0] == "0":
        raise ValueError("CIDR prefix must not contain leading zeros")
    if len(prefix) > 2:
        raise ValueError("CIDR prefix is out of range")

    number = int(prefix)
    if number > 32:
        raise ValueError("CIDR prefix is out of range")
    return number


def cidr_contains(cidr: str, ip: str) -> bool:
    """Return whether a strictly formatted IPv4 address belongs to a CIDR block."""
    if not isinstance(cidr, str):
        raise ValueError("CIDR must be a string")
    if not isinstance(ip, str):
        raise ValueError("IPv4 address must be a string")
    if cidr.count("/") != 1:
        raise ValueError("CIDR must contain exactly one slash")

    network_text, prefix_text = cidr.split("/")
    network = _parse_ipv4(network_text)
    address = _parse_ipv4(ip)
    prefix = _parse_prefix(prefix_text)

    mask = 0 if prefix == 0 else (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return (address & mask) == (network & mask)
