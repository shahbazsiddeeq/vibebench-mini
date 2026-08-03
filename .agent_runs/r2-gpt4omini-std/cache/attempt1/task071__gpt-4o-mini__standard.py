# src/solution.py

import re

def classify_ip(ip):
    # Define regex patterns for IPv4 and IPv6
    ipv4_pattern = re.compile(r'^(?:\d{1,3}\.){3}\d{1,3}$')
    ipv6_pattern = re.compile(r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,7}:|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|'
                              r'[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}|'
                              r':(?::[0-9a-fA-F]{1,4}){1,7}|'
                              r'::)$')

    # Initialize the result dictionary
    result = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False
    }

    # Check for IPv4
    if ipv4_pattern.match(ip):
        octets = list(map(int, ip.split('.')))
        if all(0 <= octet < 256 for octet in octets):
            result["valid"] = True
            result["version"] = 4
            
            # Check for private and loopback
            if (ip.startswith("10.") or
                (ip.startswith("172.") and 16 <= octets[1] <= 31) or
                (ip.startswith("192.168.")) or
                (ip.startswith("127.")) or
                (ip.startswith("169.254.")) or
                (ip == "0.0.0.0") or
                (ip == "192.0.2.0")):
                result["private"] = True
            if ip.startswith("127."):
                result["loopback"] = True

    # Check for IPv6
    elif ipv6_pattern.match(ip):
        result["valid"] = True
        result["version"] = 6
        
        # Check for private and loopback
        if (ip == "::1" or
            ip.startswith("fc") or
            ip.startswith("fd") or
            ip.startswith("fe80") or
            ip.startswith("2001:db8:")):
            result["private"] = True
        if ip == "::1":
            result["loopback"] = True

    return result
