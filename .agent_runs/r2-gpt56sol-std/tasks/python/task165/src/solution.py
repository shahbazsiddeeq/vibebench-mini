def _parse_ipv4(address: str) -> int:
    if not isinstance(address, str):
        raise ValueError("IPv4 address must be a string")

    octets = address.split(".")
    if len(octets) != 4:
        raise ValueError("IPv4 address must contain exactly four octets")

    value = 0
    for octet in octets:
        if not octet or not octet.isascii() or not octet.isdigit():
            raise ValueError("IPv4 octets must be decimal integers")
        if len(octet) > 1 and octet[0] == "0":
            raise ValueError("IPv4 octets must not contain leading zeros")

        number = int(octet)
        if number > 255:
            raise ValueError("IPv4 octet out of range")

        value = (value << 8) | number

    return value


def cidr_contains(cidr: str, ip: str) -> bool:
    if not isinstance(cidr, str) or cidr.count("/") != 1:
        raise ValueError("CIDR must contain exactly one slash")

    network_text, prefix_text = cidr.split("/")

    if (
        not prefix_text
        or not prefix_text.isascii()
        or not prefix_text.isdigit()
        or (len(prefix_text) > 1 and prefix_text[0] == "0")
    ):
        raise ValueError("Invalid CIDR prefix")

    prefix = int(prefix_text)
    if prefix > 32:
        raise ValueError("CIDR prefix out of range")

    network = _parse_ipv4(network_text)
    address = _parse_ipv4(ip)

    mask = 0 if prefix == 0 else (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return (address & mask) == (network & mask)
