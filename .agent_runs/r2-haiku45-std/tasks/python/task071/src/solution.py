import ipaddress
from typing import Dict, Union, Optional


def classify_ip(ip: str) -> Dict[str, Union[bool, Optional[int]]]:
    """
    Classify an IP address as valid/invalid, IPv4/IPv6, private/public, loopback/not.
    
    Returns a dict with keys:
    - valid (bool): whether the string is a valid IPv4 or IPv6 address
    - version (4, 6, or None): IP version if valid, None otherwise
    - private (bool): whether the address is in a reserved/not-globally-routable range
    - loopback (bool): whether the address is a loopback address
    """
    
    # Default response for invalid input
    default_response = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False
    }
    
    # Try to parse the IP address
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return default_response
    
    # Determine IP version
    if isinstance(addr, ipaddress.IPv4Address):
        version = 4
    else:  # IPv6Address
        version = 6
    
    # Check if loopback
    is_loopback = addr.is_loopback
    
    # Check if private
    # For IPv4: includes 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8,
    #           169.254.0.0/16, and special ranges like 0.0.0.0/8, 192.0.2.0/24
    # For IPv6: includes ::1, fc00::/7, fe80::/10, 2001:db8::/32
    # Note: 100.64.0.0/10 (CGNAT) is NOT private
    
    is_private = addr.is_private
    
    return {
        "valid": True,
        "version": version,
        "private": is_private,
        "loopback": is_loopback
    }
