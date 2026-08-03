# src/solution.py

def cidr_contains(cidr: str, ip: str) -> bool:
    # Validate and parse the CIDR notation
    if '/' not in cidr or cidr.count('/') != 1:
        raise ValueError("CIDR must contain exactly one '/'")
    
    network_part, prefix_part = cidr.split('/')
    
    # Validate the prefix
    if not prefix_part.isdigit() or not (0 <= int(prefix_part) <= 32):
        raise ValueError("Prefix must be an integer between 0 and 32 with no leading zeros")
    
    prefix = int(prefix_part)
    
    # Validate the network part
    octets = network_part.split('.')
    if len(octets) != 4:
        raise ValueError("Network part must contain exactly four octets")
    
    network_int = 0
    for octet in octets:
        if not octet.isdigit() or not (0 <= int(octet) <= 255) or (len(octet) > 1 and octet[0] == '0'):
            raise ValueError("Each octet must be an integer 0-255 with no leading zeros")
        network_int = (network_int << 8) | int(octet)
    
    # Validate the IP address
    ip_octets = ip.split('.')
    if len(ip_octets) != 4:
        raise ValueError("IP must contain exactly four octets")
    
    ip_int = 0
    for octet in ip_octets:
        if not octet.isdigit() or not (0 <= int(octet) <= 255) or (len(octet) > 1 and octet[0] == '0'):
            raise ValueError("Each octet must be an integer 0-255 with no leading zeros")
        ip_int = (ip_int << 8) | int(octet)
    
    # Calculate the mask
    if prefix == 0:
        mask = 0
    else:
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    
    # Check if the IP is in the CIDR range
    return (ip_int & mask) == (network_int & mask)
