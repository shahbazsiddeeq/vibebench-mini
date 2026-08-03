def _parse_ipv4_octet(octet_str: str) -> int:
    """Parses a single IPv4 octet string, validating its format and range."""
    if not octet_str.isdigit():
        raise ValueError(f"Invalid octet: '{octet_str}' is not a number.")
    if len(octet_str) > 1 and octet_str.startswith('0'):
        raise ValueError(f"Invalid octet: '{octet_str}' has leading zeros.")
    octet = int(octet_str)
    if not (0 <= octet <= 255):
        raise ValueError(f"Invalid octet: {octet} is out of range (0-255).")
    return octet

def _parse_ipv4_address(ip_str: str) -> int:
    """Parses an IPv4 address string into a 32-bit integer."""
    octets_str = ip_str.split('.')
    if len(octets_str) != 4:
        raise ValueError(f"Invalid IP address: '{ip_str}' does not have 4 octets.")
    
    ip_int = 0
    for i, octet_str in enumerate(octets_str):
        octet = _parse_ipv4_octet(octet_str)
        ip_int |= (octet << (24 - i * 8))
    return ip_int

def cidr_contains(cidr: str, ip: str) -> bool:
    """
    Checks if an IPv4 address lies within an IPv4 CIDR block.

    Args:
        cidr: The CIDR block string (e.g., '192.168.1.0/24').
        ip: The IPv4 address string (e.g., '192.168.1.42').

    Returns:
        True if the IP address is within the CIDR block, False otherwise.

    Raises:
        ValueError: On any malformed cidr or ip string.
    """
    # Parse CIDR
    parts = cidr.split('/')
    if len(parts) != 2:
        raise ValueError(f"Invalid CIDR: '{cidr}' must have exactly one '/'.")
    
    network_str, prefix_str = parts[0], parts[1]

    network_int = _parse_ipv4_address(network_str)

    if not prefix_str.isdigit():
        raise ValueError(f"Invalid prefix: '{prefix_str}' is not an integer.")
    if len(prefix_str) > 1 and prefix_str.startswith('0'):
        raise ValueError(f"Invalid prefix: '{prefix_str}' has leading zeros.")
    
    prefix = int(prefix_str)
    if not (0 <= prefix <= 32):
        raise ValueError(f"Invalid prefix: {prefix} is out of range (0-32).")

    # Calculate mask
    if prefix == 0:
        mask = 0
    else:
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

    # Parse IP
    ip_int = _parse_ipv4_address(ip)

    # Compare
    return (ip_int & mask) == (network_int & mask)
