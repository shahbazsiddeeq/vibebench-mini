# src/solution.py

def parse_cookie(header):
    if not isinstance(header, str):
        raise ValueError("Input must be a string")

    cookies = {}
    pairs = header.split(';')
    
    for pair in pairs:
        pair = pair.strip()
        if '=' in pair:
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key:
                cookies[key] = value

    return cookies
