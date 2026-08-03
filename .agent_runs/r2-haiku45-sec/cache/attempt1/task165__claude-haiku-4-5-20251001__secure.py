"""IPv4 CIDR membership checker with strict validation."""


def cidr_contains(cidr: str, ip: str) -> bool:
    """
    Check if an IPv4 address lies within a CIDR block.
    
    Args:
        cidr: IPv4 CIDR block in format 'network/prefix' (e.g., '192.168.1.0/24')
        ip: IPv4 address in dotted-decimal format (e.g., '192.168.1.42')
    
    Returns:
        True if ip is within the CIDR block, False otherwise.
    
    Raises:
        ValueError: If cidr or ip is malformed.
    """
    # Parse CIDR
    network_int, prefix = _parse_cidr(cidr)
    
    # Parse IP
    ip_int = _parse_ip(ip)
    
    # Compute mask
    mask = _compute_mask(prefix)
    
    # Check membership
    return (ip_int & mask) == (network_int & mask)


def _parse_cidr(cidr: str) -> tuple:
    """
    Parse CIDR notation into network integer and prefix length.
    
    Args:
        cidr: String in format 'network/prefix'
    
    Returns:
        Tuple of (network_int, prefix_length)
    
    Raises:
        ValueError: If format is invalid.
    """
    if not isinstance(cidr, str):
        raise ValueError("CIDR must be a string")
    
    # Check for exactly one '/'
    slash_count = cidr.count('/')
    if slash_count != 1:
        raise ValueError("CIDR must contain exactly one '/'")
    
    parts = cidr.split('/')
    network_part = parts[0]
    prefix_part = parts[1]
    
    # Parse network part
    network_int = _parse_ip(network_part)
    
    # Parse prefix part
    prefix = _parse_prefix(prefix_part)
    
    return network_int, prefix


def _parse_ip(ip: str) -> int:
    """
    Parse IPv4 address in dotted-decimal notation to integer.
    
    Args:
        ip: IPv4 address string (e.g., '192.168.1.1')
    
    Returns:
        Integer representation of the IP address.
    
    Raises:
        ValueError: If format is invalid.
    """
    if not isinstance(ip, str):
        raise ValueError("IP must be a string")
    
    octets = ip.split('.')
    
    # Must have exactly 4 octets
    if len(octets) != 4:
        raise ValueError("IP must have exactly 4 octets")
    
    result = 0
    for octet_str in octets:
        octet = _parse_octet(octet_str)
        result = (result << 8) | octet
    
    return result


def _parse_octet(octet_str: str) -> int:
    """
    Parse a single octet with strict validation.
    
    Args:
        octet_str: String representation of an octet
    
    Returns:
        Integer value of the octet (0-255)
    
    Raises:
        ValueError: If octet is invalid.
    """
    if not isinstance(octet_str, str):
        raise ValueError("Octet must be a string")
    
    if len(octet_str) == 0:
        raise ValueError("Octet cannot be empty")
    
    # Check for leading zeros (but '0' itself is valid)
    if len(octet_str) > 1 and octet_str[0] == '0':
        raise ValueError("Octet cannot have leading zeros")
    
    # Check that all characters are digits
    if not octet_str.isdigit():
        raise ValueError("Octet must contain only digits")
    
    octet = int(octet_str)
    
    # Check range
    if octet < 0 or octet > 255:
        raise ValueError("Octet must be between 0 and 255")
    
    return octet


def _parse_prefix(prefix_str: str) -> int:
    """
    Parse prefix length with strict validation.
    
    Args:
        prefix_str: String representation of prefix length
    
    Returns:
        Integer prefix length (0-32)
    
    Raises:
        ValueError: If prefix is invalid.
    """
    if not isinstance(prefix_str, str):
        raise ValueError("Prefix must be a string")
    
    if len(prefix_str) == 0:
        raise ValueError("Prefix cannot be empty")
    
    # Check for leading zeros (but '0' itself is valid)
    if len(prefix_str) > 1 and prefix_str[0] == '0':
        raise ValueError("Prefix cannot have leading zeros")
    
    # Check that all characters are digits
    if not prefix_str.isdigit():
        raise ValueError("Prefix must be a non-negative integer")
    
    prefix = int(prefix_str)
    
    # Check range
    if prefix < 0 or prefix > 32:
        raise ValueError("Prefix must be between 0 and 32")
    
    return prefix


def _compute_mask(prefix: int) -> int:
    """
    Compute the network mask for a given prefix length.
    
    Args:
        prefix: Prefix length (0-32)
    
    Returns:
        32-bit network mask
    """
    if prefix == 0:
        return 0
    if prefix == 32:
        return 0xFFFFFFFF
    
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return mask
