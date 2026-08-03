import ipaddress


def classify_ip(ip):
    result = {"valid": False, "version": None, "private": False, "loopback": False}
    if not isinstance(ip, str):
        return result
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return result

    result["valid"] = True
    result["version"] = addr.version
    result["private"] = addr.is_private
    result["loopback"] = addr.is_loopback
    return result
