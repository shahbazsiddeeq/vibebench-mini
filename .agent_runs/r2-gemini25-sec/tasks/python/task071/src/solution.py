import re

def _is_ipv4_private(ip_parts):
    """
    Checks if an IPv4 address is private based on IANA special-purpose address registries.
    """
    first_octet = int(ip_parts[0])
    second_octet = int(ip_parts[1])

    # 10.0.0.0/8
    if first_octet == 10:
        return True
    # 172.16.0.0/12
    if first_octet == 172 and 16 <= second_octet <= 31:
        return True
    # 192.168.0.0/16
    if first_octet == 192 and second_octet == 168:
        return True
    # 127.0.0.0/8 (loopback) - handled by loopback check, but also private
    if first_octet == 127:
        return True
    # 169.254.0.0/16 (link-local)
    if first_octet == 169 and second_octet == 254:
        return True
    # 0.0.0.0/8 (current network)
    if first_octet == 0:
        return True
    # 192.0.2.0/24 (TEST-NET-1)
    if first_octet == 192 and second_octet == 0 and int(ip_parts[2]) == 2:
        return True
    # 198.51.100.0/24 (TEST-NET-2)
    if first_octet == 198 and second_octet == 51 and int(ip_parts[2]) == 100:
        return True
    # 203.0.113.0/24 (TEST-NET-3)
    if first_octet == 203 and second_octet == 0 and int(ip_parts[2]) == 113:
        return True
    # 224.0.0.0/4 (Multicast) - often considered private in some contexts, but not strictly by IANA for general private use
    # For this task, we stick to the explicit ranges mentioned.
    # 240.0.0.0/4 (Reserved for future use)
    if first_octet >= 240:
        return True

    return False

def _is_ipv6_private(ip_str_normalized):
    """
    Checks if an IPv6 address is private based on IANA special-purpose address registries.
    """
    # ::1 (loopback) - handled by loopback check, but also private
    if ip_str_normalized == "::1":
        return True
    # fc00::/7 (Unique Local Unicast)
    if ip_str_normalized.startswith("fc") or ip_str_normalized.startswith("fd"):
        return True
    # fe80::/10 (Link-Local Unicast)
    if ip_str_normalized.startswith("fe8") or ip_str_normalized.startswith("fe9") or \
       ip_str_normalized.startswith("fea") or ip_str_normalized.startswith("feb"):
        return True
    # 2001:db8::/32 (Documentation)
    if ip_str_normalized.startswith("2001:db8:"):
        return True
    return False

def _is_ipv4_loopback(ip_parts):
    """
    Checks if an IPv4 address is a loopback address (127.0.0.0/8).
    """
    return int(ip_parts[0]) == 127

def _is_ipv6_loopback(ip_str_normalized):
    """
    Checks if an IPv6 address is a loopback address (::1).
    """
    return ip_str_normalized == "::1"

def classify_ip(ip):
    """
    Classifies an IP address string, returning its validity, version,
    private status, and loopback status.
    """
    result = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False
    }

    if not isinstance(ip, str):
        return result

    # Regex for IPv4: four octets, each 0-255. No CIDR, no port.
    ipv4_pattern = re.compile(
        r"^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\."
        r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\."
        r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\."
        r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])$"
    )

    # Regex for IPv6: more complex, allows for zero compression (::)
    # This pattern is a simplification and might not catch all edge cases
    # but covers common valid forms without CIDR or port.
    # It checks for up to 8 groups of 1-4 hex digits, separated by colons.
    # It also handles the '::' compression.
    # This is a more robust regex than a simple split and count.
    # Source: https://www.regular-expressions.info/ipv6.html (simplified for no CIDR/port)
    ipv6_pattern = re.compile(
        r"^("
        r"([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|"  # 1:2:3:4:5:6:7:8
        r"([0-9a-fA-F]{1,4}:){1,7}:|"                 # 1::                          1:2:3::
        r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|" # 1::8, 1:2:3::8
        r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|" # 1::7:8, 1:2:3::7:8
        r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|" # 1::6:7:8, 1:2:3::6:7:8
        r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|" # 1::5:6:7:8, 1:2:3::5:6:7:8
        r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|" # 1::4:5:6:7:8, 1:2:3::4:5:6:7:8
        r"[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|" # 1::3:4:5:6:7:8
        r":((:[0-9a-fA-F]{1,4}){1,7}|:)|"             # ::2:3:4:5:6:7:8, ::
        r"fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|" # fe80::7:8%eth0 (zone id) - simplified to exclude %zone
        r"::(ffff(:0{1,4}){0,1}:){0,1}"
        r"((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.){3,3}"
        r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])|" # ::255.255.255.255, ::ffff:255.255.255.255, ::ffff:0:255.255.255.255
        r"([0-9a-fA-F]{1,4}:){1,4}:"
        r"((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.){3,3}"
        r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])" # 2001:db8:3:4::192.0.2.33
        r")$",
        re.IGNORECASE
    )


    if ipv4_pattern.match(ip):
        result["valid"] = True
        result["version"] = 4
        ip_parts = ip.split('.')
        result["loopback"] = _is_ipv4_loopback(ip_parts)
        result["private"] = _is_ipv4_private(ip_parts)
    elif ipv6_pattern.match(ip):
        result["valid"] = True
        result["version"] = 6
        # Normalize IPv6 for easier comparison (e.g., expand '::', lowercase hex)
        # This is a simplified normalization for specific checks.
        # A full normalization is complex and usually handled by ipaddress module.
        # For this task, we only need to check prefixes and ::1.
        # We'll use the original string for prefix checks, and a specific check for ::1.
        
        # For ::1 check, direct comparison is fine.
        if ip == "::1":
            result["loopback"] = True
            result["private"] = True # ::1 is also private

        # For other IPv6 private ranges, we need to check prefixes.
        # Convert to lowercase for consistent prefix matching.
        ip_lower = ip.lower()
        if _is_ipv6_private(ip_lower):
            result["private"] = True
    
    return result
