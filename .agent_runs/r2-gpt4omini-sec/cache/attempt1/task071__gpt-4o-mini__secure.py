# src/solution.py

import re
import ipaddress

def classify_ip(ip: str) -> dict:
    # Initialize the response dictionary
    response = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False
    }
    
    # Validate input
    if not isinstance(ip, str):
        return response
    
    # Check for IPv4
    try:
        ipv4 = ipaddress.ip_address(ip)
        if isinstance(ipv4, ipaddress.IPv4Address):
            response["valid"] = True
            response["version"] = 4
            
            # Check for private and loopback
            response["private"] = ipv4.is_private
            response["loopback"] = ipv4.is_loopback
            
    except ValueError:
        # Not a valid IP address
        pass
    
    # Check for IPv6
    try:
        ipv6 = ipaddress.ip_address(ip)
        if isinstance(ipv6, ipaddress.IPv6Address):
            response["valid"] = True
            response["version"] = 6
            
            # Check for private and loopback
            response["private"] = ipv6.is_private
            response["loopback"] = ipv6.is_loopback
            
    except ValueError:
        # Not a valid IP address
        pass
    
    return response
