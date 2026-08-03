# src/solution.py

def parse_cookie(header: str) -> dict:
    if not isinstance(header, str):
        raise ValueError("Header must be a string")

    cookies = {}
    pairs = header.split(';')

    for pair in pairs:
        # Split on the first '=' only
        if '=' in pair:
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key:  # Ignore segments with no key
                cookies[key] = value

    return cookies
