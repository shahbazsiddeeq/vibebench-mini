# src/solution.py

import ipaddress

def classify_ip(ip):
    result = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False
    }
    
    try:
        ip_obj = ipaddress.ip_address(ip)
        result["valid"] = True
        result["version"] = 4 if isinstance(ip_obj, ipaddress.IPv4Address) else 6
        result["private"] = ip_obj.is_private
        result["loopback"] = ip_obj.is_loopback
    except ValueError:
        pass
    
    return result
