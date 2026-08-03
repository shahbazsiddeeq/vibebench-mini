# src/solution.py

def parse_cookie(header: str) -> dict:
    cookies = {}
    pairs = header.split(';')
    
    for pair in pairs:
        # Split on the first '=' only
        if '=' in pair:
            key, value = pair.split('=', 1)
            # Trim whitespace
            key = key.strip()
            value = value.strip()
            # Ignore segments with no '='
            if key:
                cookies[key] = value
    
    return cookies
