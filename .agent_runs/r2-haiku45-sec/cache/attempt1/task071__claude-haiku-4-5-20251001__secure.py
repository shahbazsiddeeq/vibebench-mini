import ipaddress
from typing import Any


def classify_ip(ip: Any) -> dict:
    """
    Classify an IP address as valid/invalid, IPv4/IPv6, private, and loopback.
    
    Args:
        ip: A string representing an IP address
        
    Returns:
        A dict with keys: valid (bool), version (4, 6, or None), 
        private (bool), loopback (bool)
    """
    # Default response for invalid input
    default_response = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False
    }
    
    # Validate input type
    if not isinstance(ip, str):
        return default_response
    
    # Try to parse the IP address
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return default_response
    
    # Determine IP version
    if isinstance(addr, ipaddress.IPv4Address):
        version = 4
    elif isinstance(addr, ipaddress.IPv6Address):
        version = 6
    else:
        return default_response
    
    # Check if loopback
    is_loopback = addr.is_loopback
    
    # Check if private
    # is_private in ipaddress module matches IANA special-purpose registries
    is_private = addr.is_private
    
    return {
        "valid": True,
        "version": version,
        "private": is_private,
        "loopback": is_loopback
    }
