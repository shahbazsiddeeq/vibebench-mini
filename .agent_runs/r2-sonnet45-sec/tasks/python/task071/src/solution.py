import ipaddress


def classify_ip(ip):
    """
    Classify an IP address string.
    
    Returns a dict with keys:
    - valid (bool): whether the string is a valid IPv4 or IPv6 address
    - version (int or None): 4 for IPv4, 6 for IPv6, None if invalid
    - private (bool): True if in reserved/non-globally-routable range
    - loopback (bool): True if loopback address
    
    Args:
        ip: String representation of an IP address
        
    Returns:
        dict with classification results
    """
    # Default result for invalid input
    result = {
        "valid": False,
        "version": None,
        "private": False,
        "loopback": False
    }
    
    # Validate input type
    if not isinstance(ip, str):
        return result
    
    # Sanitize input - strip whitespace
    ip = ip.strip()
    
    # Prevent empty strings
    if not ip:
        return result
    
    try:
        # Parse the IP address
        addr = ipaddress.ip_address(ip)
        
        # Valid IP address found
        result["valid"] = True
        result["version"] = addr.version
        result["loopback"] = addr.is_loopback
        
        # Determine if private
        # The ipaddress module's is_private includes most ranges we want,
        # but we need to handle CGNAT specially
        if addr.version == 4:
            # Check if it's in CGNAT range (100.64.0.0/10)
            cgnat_network = ipaddress.IPv4Network('100.64.0.0/10')
            is_cgnat = addr in cgnat_network
            
            # Use is_private but exclude CGNAT
            if is_cgnat:
                result["private"] = False
            else:
                result["private"] = addr.is_private
        else:
            # For IPv6, use is_private directly
            result["private"] = addr.is_private
            
    except ValueError:
        # Invalid IP address format
        pass
    except Exception:
        # Catch any other unexpected errors
        pass
    
    return result
