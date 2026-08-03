def cidr_contains(cidr: str, ip: str) -> bool:
    """
    Returns True iff the IPv4 address ip lies within the IPv4 block cidr.
    
    Args:
        cidr: Network in CIDR notation (e.g., '192.168.1.0/24')
        ip: IPv4 address (e.g., '192.168.1.42')
    
    Returns:
        bool: True if ip is within the cidr block, False otherwise
    
    Raises:
        ValueError: If cidr or ip is malformed
    """
    # Validate and parse CIDR
    if not isinstance(cidr, str) or not isinstance(ip, str):
        raise ValueError("cidr and ip must be strings")
    
    # Check for exactly one slash in CIDR
    if cidr.count('/') != 1:
        raise ValueError("CIDR must contain exactly one '/'")
    
    network_str, prefix_str = cidr.split('/')
    
    # Parse and validate prefix length
    prefix = _parse_prefix(prefix_str)
    
    # Parse and validate network address
    network_int = _parse_ipv4(network_str)
    
    # Parse and validate IP address
    ip_int = _parse_ipv4(ip)
    
    # Calculate mask
    if prefix == 0:
        mask = 0
    else:
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    
    # Check membership
    return (ip_int & mask) == (network_int & mask)


def _parse_prefix(prefix_str: str) -> int:
    """
    Parse and validate prefix length.
    
    Args:
        prefix_str: String representation of prefix length
    
    Returns:
        int: Validated prefix length (0-32)
    
    Raises:
        ValueError: If prefix is invalid
    """
    if not prefix_str:
        raise ValueError("Prefix length cannot be empty")
    
    # Check for leading zeros (except "0" itself)
    if len(prefix_str) > 1 and prefix_str[0] == '0':
        raise ValueError("Prefix length cannot have leading zeros")
    
    # Check that all characters are digits
    if not prefix_str.isdigit():
        raise ValueError("Prefix length must be an integer")
    
    try:
        prefix = int(prefix_str)
    except ValueError:
        raise ValueError("Prefix length must be an integer")
    
    if prefix < 0 or prefix > 32:
        raise ValueError("Prefix length must be between 0 and 32")
    
    return prefix


def _parse_ipv4(ip_str: str) -> int:
    """
    Parse and validate an IPv4 address.
    
    Args:
        ip_str: String representation of IPv4 address
    
    Returns:
        int: 32-bit integer representation of the IP address
    
    Raises:
        ValueError: If IP address is malformed
    """
    if not ip_str:
        raise ValueError("IP address cannot be empty")
    
    parts = ip_str.split('.')
    
    # Must have exactly 4 octets
    if len(parts) != 4:
        raise ValueError("IP address must have exactly 4 octets")
    
    octets = []
    for part in parts:
        octet = _parse_octet(part)
        octets.append(octet)
    
    # Convert to 32-bit integer
    ip_int = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
    return ip_int


def _parse_octet(octet_str: str) -> int:
    """
    Parse and validate a single octet.
    
    Args:
        octet_str: String representation of an octet
    
    Returns:
        int: Validated octet value (0-255)
    
    Raises:
        ValueError: If octet is invalid
    """
    if not octet_str:
        raise ValueError("Octet cannot be empty")
    
    # Check for leading zeros (except "0" itself)
    if len(octet_str) > 1 and octet_str[0] == '0':
        raise ValueError("Octet cannot have leading zeros")
    
    # Check that all characters are digits
    if not octet_str.isdigit():
        raise ValueError("Octet must be an integer")
    
    try:
        octet = int(octet_str)
    except ValueError:
        raise ValueError("Octet must be an integer")
    
    if octet < 0 or octet > 255:
        raise ValueError("Octet must be between 0 and 255")
    
    return octet
