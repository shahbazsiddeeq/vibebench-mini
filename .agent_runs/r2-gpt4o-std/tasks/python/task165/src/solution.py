# src/solution.py

def cidr_contains(cidr: str, ip: str) -> bool:
    def validate_ip(ip: str) -> int:
        parts = ip.split('.')
        if len(parts) != 4:
            raise ValueError("IP address must have exactly four octets.")
        ip_int = 0
        for part in parts:
            if not part.isdigit() or (part != '0' and part.startswith('0')):
                raise ValueError("Each octet must be a non-negative integer with no leading zeros.")
            octet = int(part)
            if octet < 0 or octet > 255:
                raise ValueError("Each octet must be in the range 0-255.")
            ip_int = (ip_int << 8) | octet
        return ip_int

    def validate_cidr(cidr: str) -> (int, int):
        try:
            network, prefix = cidr.split('/')
        except ValueError:
            raise ValueError("CIDR must contain exactly one '/' character.")
        
        network_int = validate_ip(network)
        
        if not prefix.isdigit() or (prefix != '0' and prefix.startswith('0')):
            raise ValueError("Prefix length must be a non-negative integer with no leading zeros.")
        
        prefix_length = int(prefix)
        if prefix_length < 0 or prefix_length > 32:
            raise ValueError("Prefix length must be in the range 0-32.")
        
        return network_int, prefix_length

    network_int, prefix_length = validate_cidr(cidr)
    ip_int = validate_ip(ip)

    mask = (0xFFFFFFFF << (32 - prefix_length)) & 0xFFFFFFFF
    return (ip_int & mask) == (network_int & mask)
