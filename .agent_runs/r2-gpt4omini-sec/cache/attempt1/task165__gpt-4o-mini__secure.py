# src/solution.py

import re
import ipaddress

def cidr_contains(cidr: str, ip: str) -> bool:
    # Validate CIDR format
    if not isinstance(cidr, str) or not isinstance(ip, str):
        raise ValueError("CIDR and IP must be strings.")
    
    # Check for exactly one '/'
    if cidr.count('/') != 1:
        raise ValueError("CIDR must contain exactly one '/'.")

    network_part, prefix_part = cidr.split('/')
    
    # Validate network part
    if not re.match(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', network_part):
        raise ValueError("Invalid network part in CIDR.")
    
    # Validate prefix part
    if not prefix_part.isdigit() or not (0 <= int(prefix_part) <= 32):
        raise ValueError("Prefix must be an integer between 0 and 32.")
    
    # Check for leading zeros in prefix
    if prefix_part != '0' and prefix_part.startswith('0'):
        raise ValueError("Prefix must not have leading zeros.")
    
    # Validate IP address
    if not re.match(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ip):
        raise ValueError("Invalid IP address.")
    
    # Convert to integers
    network_int = int(ipaddress.IPv4Address(network_part))
    ip_int = int(ipaddress.IPv4Address(ip))
    prefix_length = int(prefix_part)
    
    # Calculate the mask
    mask = (0xFFFFFFFF << (32 - prefix_length)) & 0xFFFFFFFF
    
    # Check membership
    return (ip_int & mask) == (network_int & mask)
