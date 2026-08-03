def parse_cookie(header: str) -> dict:
    cookies = {}
    pairs = header.split(';')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()
            cookies[key] = value
    return cookies
