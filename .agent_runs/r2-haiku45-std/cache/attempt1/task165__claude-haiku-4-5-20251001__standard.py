def cidr_contains(cidr: str, ip: str) -> bool:
    """
    Check if an IPv4 address lies within a CIDR block.
    
    Args:
        cidr: IPv4 CIDR notation (e.g., '192.168.1.0/24')
        ip: IPv4 address (e.g., '192.168.1.42')
    
    Returns:
        True if ip is within the CIDR block, False otherwise
    
    Raises:
        ValueError: If cidr or ip is malformed
    """
    
    def parse_ipv4(ip_str: str) -> int:
        """Parse IPv4 address string to 32-bit integer."""
        parts = ip_str.split('.')
        if len(parts) != 4:
            raise ValueError(f"Invalid IPv4 address: {ip_str}")
        
        result = 0
        for part in parts:
            # Check for empty part
            if not part:
                raise ValueError(f"Invalid IPv4 address: {ip_str}")
            
            # Check for leading zeros (but '0' itself is valid)
            if len(part) > 1 and part[0] == '0':
                raise ValueError(f"Invalid IPv4 address: {ip_str}")
            
            # Check if it's a valid integer
            try:
                octet = int(part)
            except ValueError:
                raise ValueError(f"Invalid IPv4 address: {ip_str}")
            
            # Check range
            if octet < 0 or octet > 255:
                raise ValueError(f"Invalid IPv4 address: {ip_str}")
            
            result = (result << 8) | octet
        
        return result
    
    # Parse CIDR
    if cidr.count('/') != 1:
        raise ValueError(f"Invalid CIDR: {cidr}")
    
    network_str, prefix_str = cidr.split('/')
    
    # Parse prefix length
    if not prefix_str:
        raise ValueError(f"Invalid CIDR: {cidr}")
    
    # Check for leading zeros in prefix (but '0' itself is valid)
    if len(prefix_str) > 1 and prefix_str[0] == '0':
        raise ValueError(f"Invalid CIDR: {cidr}")
    
    try:
        prefix = int(prefix_str)
    except ValueError:
        raise ValueError(f"Invalid CIDR: {cidr}")
    
    if prefix < 0 or prefix > 32:
        raise ValueError(f"Invalid CIDR: {cidr}")
    
    # Parse network address
    network_int = parse_ipv4(network_str)
    
    # Parse IP address
    ip_int = parse_ipv4(ip)
    
    # Calculate mask
    if prefix == 0:
        mask = 0
    else:
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    
    # Check membership
    return (ip_int & mask) == (network_int & mask)
