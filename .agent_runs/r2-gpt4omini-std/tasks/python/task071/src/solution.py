# src/solution.py

import re

def classify_ip(ip):
    # Regular expressions for IPv4 and IPv6
    ipv4_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    ipv6_pattern = re.compile(r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,7}:|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|'
                              r'(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|'
                              r'[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}|'
                              r':(?::[0-9a-fA-F]{1,4}){1,7}|::)$')

    # Check if the IP is valid
    if ipv4_pattern.match(ip):
        return classify_ipv4(ip)
    elif ipv6_pattern.match(ip):
        return classify_ipv6(ip)
    else:
        return {"valid": False, "version": None, "private": False, "loopback": False}

def classify_ipv4(ip):
    octets = list(map(int, ip.split('.')))
    valid = all(0 <= octet < 256 for octet in octets)
    private = (ip.startswith("10.") or
               ip.startswith("172.") and 16 <= octets[1] <= 31 or
               ip.startswith("192.168.") or
               ip.startswith("127.") or
               ip.startswith("169.254."))
    loopback = ip.startswith("127.")
    
    return {
        "valid": valid,
        "version": 4,
        "private": private,
        "loopback": loopback
    }

def classify_ipv6(ip):
    private = (ip.startswith("fc00:") or
               ip.startswith("fe80:") or
               ip == "::1" or
               ip.startswith("2001:db8:"))
    loopback = (ip == "::1")
    
    return {
        "valid": True,
        "version": 6,
        "private": private,
        "loopback": loopback
    }
