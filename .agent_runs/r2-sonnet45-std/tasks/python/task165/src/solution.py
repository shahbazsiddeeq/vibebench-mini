def cidr_contains(cidr: str, ip: str) -> bool:
    """
    Returns True iff the IPv4 address ip lies within the IPv4 block cidr.
    
    Args:
        cidr: CIDR notation string (e.g., '192.168.1.0/24')
        ip: IPv4 address string (e.g., '192.168.1.42')
    
    Returns:
        bool: True if ip is in the CIDR block, False otherwise
    
    Raises:
        ValueError: If cidr or ip is malformed
    """
    
    def parse_octet(octet_str: str) -> int:
        """Parse a single octet with strict validation."""
        # Check for leading zeros (except "0" itself)
        if len(octet_str) > 1 and octet_str[0] == '0':
            raise ValueError(f"Leading zero in octet: {octet_str}")
        
        # Check if it's a valid integer
        try:
            value = int(octet_str)
        except ValueError:
            raise ValueError(f"Invalid octet: {octet_str}")
        
        # Check range
        if value < 0 or value > 255:
            raise ValueError(f"Octet out of range: {value}")
        
        return value
    
    def parse_ip(ip_str: str) -> int:
        """Parse an IPv4 address to an integer."""
        parts = ip_str.split('.')
        
        if len(parts) != 4:
            raise ValueError(f"IP must have exactly 4 octets: {ip_str}")
        
        octets = [parse_octet(part) for part in parts]
        
        # Convert to 32-bit integer
        result = 0
        for octet in octets:
            result = (result << 8) | octet
        
        return result
    
    def parse_prefix(prefix_str: str) -> int:
        """Parse prefix length with strict validation."""
        # Check for leading zeros (except "0" itself)
        if len(prefix_str) > 1 and prefix_str[0] == '0':
            raise ValueError(f"Leading zero in prefix: {prefix_str}")
        
        # Check if it's a valid integer
        try:
            value = int(prefix_str)
        except ValueError:
            raise ValueError(f"Invalid prefix: {prefix_str}")
        
        # Check range
        if value < 0 or value > 32:
            raise ValueError(f"Prefix out of range: {value}")
        
        return value
    
    # Parse CIDR
    parts = cidr.split('/')
    
    if len(parts) != 2:
        raise ValueError(f"CIDR must have exactly one '/': {cidr}")
    
    network_str, prefix_str = parts
    
    # Parse network address and prefix
    network_int = parse_ip(network_str)
    prefix = parse_prefix(prefix_str)
    
    # Parse IP address
    ip_int = parse_ip(ip)
    
    # Calculate mask
    if prefix == 0:
        mask = 0
    else:
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    
    # Check membership
    return (ip_int & mask) == (network_int & mask)
