def classify_ip(ip):
    """
    Classify an IP address string.
    
    Returns a dict with keys:
    - valid (bool): whether the string is a valid IPv4 or IPv6 address
    - version (int or None): 4, 6, or None
    - private (bool): whether the address is in a private/reserved range
    - loopback (bool): whether the address is a loopback address
    """
    result = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False
    }
    
    # Try IPv4 first
    if _is_valid_ipv4(ip):
        result["valid"] = True
        result["version"] = 4
        result["private"] = _is_private_ipv4(ip)
        result["loopback"] = _is_loopback_ipv4(ip)
        return result
    
    # Try IPv6
    if _is_valid_ipv6(ip):
        result["valid"] = True
        result["version"] = 6
        result["private"] = _is_private_ipv6(ip)
        result["loopback"] = _is_loopback_ipv6(ip)
        return result
    
    return result


def _is_valid_ipv4(ip):
    """Check if string is a valid IPv4 address."""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    
    for part in parts:
        if not part:
            return False
        # Check for leading zeros (except "0" itself)
        if len(part) > 1 and part[0] == '0':
            return False
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
    
    return True


def _is_valid_ipv6(ip):
    """Check if string is a valid IPv6 address."""
    # Handle :: compression
    if ':::' in ip:
        return False
    
    # Count :: occurrences (max 1)
    double_colon_count = ip.count('::')
    if double_colon_count > 1:
        return False
    
    # Split by ::
    if '::' in ip:
        parts = ip.split('::')
        if len(parts) != 2:
            return False
        left = parts[0].split(':') if parts[0] else []
        right = parts[1].split(':') if parts[1] else []
        
        # Remove empty strings
        left = [p for p in left if p]
        right = [p for p in right if p]
        
        total_groups = len(left) + len(right)
        if total_groups > 7:
            return False
        
        all_groups = left + right
    else:
        all_groups = ip.split(':')
        if len(all_groups) != 8:
            return False
    
    # Validate each group
    for group in all_groups:
        if not group:
            return False
        if len(group) > 4:
            return False
        try:
            int(group, 16)
        except ValueError:
            return False
    
    return True


def _ipv4_to_int(ip):
    """Convert IPv4 address to integer."""
    parts = ip.split('.')
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])


def _is_in_ipv4_range(ip, network, prefix_len):
    """Check if IPv4 address is in the given network range."""
    ip_int = _ipv4_to_int(ip)
    network_int = _ipv4_to_int(network)
    mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    return (ip_int & mask) == (network_int & mask)


def _is_private_ipv4(ip):
    """Check if IPv4 address is private according to IANA registries."""
    # Private ranges
    private_ranges = [
        ('10.0.0.0', 8),
        ('172.16.0.0', 12),
        ('192.168.0.0', 16),
        ('127.0.0.0', 8),  # Loopback
        ('169.254.0.0', 16),  # Link-local
        ('0.0.0.0', 8),  # "This network"
        ('192.0.0.0', 24),  # IETF Protocol Assignments
        ('192.0.2.0', 24),  # TEST-NET-1
        ('198.51.100.0', 24),  # TEST-NET-2
        ('203.0.113.0', 24),  # TEST-NET-3
        ('224.0.0.0', 4),  # Multicast
        ('240.0.0.0', 4),  # Reserved
        ('255.255.255.255', 32),  # Broadcast
    ]
    
    for network, prefix_len in private_ranges:
        if _is_in_ipv4_range(ip, network, prefix_len):
            return True
    
    return False


def _is_loopback_ipv4(ip):
    """Check if IPv4 address is loopback (127.0.0.0/8)."""
    return _is_in_ipv4_range(ip, '127.0.0.0', 8)


def _ipv6_to_int(ip):
    """Convert IPv6 address to integer."""
    # Expand :: notation
    if '::' in ip:
        parts = ip.split('::')
        left = parts[0].split(':') if parts[0] else []
        right = parts[1].split(':') if parts[1] else []
        
        left = [p for p in left if p]
        right = [p for p in right if p]
        
        missing = 8 - len(left) - len(right)
        groups = left + ['0'] * missing + right
    else:
        groups = ip.split(':')
    
    result = 0
    for group in groups:
        result = (result << 16) + int(group, 16)
    
    return result


def _is_in_ipv6_range(ip, network, prefix_len):
    """Check if IPv6 address is in the given network range."""
    ip_int = _ipv6_to_int(ip)
    network_int = _ipv6_to_int(network)
    mask = (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF << (128 - prefix_len)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    return (ip_int & mask) == (network_int & mask)


def _is_private_ipv6(ip):
    """Check if IPv6 address is private according to IANA registries."""
    # Private/special ranges
    private_ranges = [
        ('::1', 128),  # Loopback
        ('fc00::', 7),  # Unique local addresses
        ('fe80::', 10),  # Link-local
        ('2001:db8::', 32),  # Documentation
        ('::', 128),  # Unspecified
        ('::ffff:0:0', 96),  # IPv4-mapped
        ('100::', 64),  # Discard prefix
        ('2001::', 32),  # TEREDO (deprecated but still special)
        ('2001:10::', 28),  # Deprecated
        ('2001:20::', 28),  # ORCHIDv2
        ('ff00::', 8),  # Multicast
    ]
    
    for network, prefix_len in private_ranges:
        if _is_in_ipv6_range(ip, network, prefix_len):
            return True
    
    return False


def _is_loopback_ipv6(ip):
    """Check if IPv6 address is loopback (::1)."""
    return _ipv6_to_int(ip) == 1
