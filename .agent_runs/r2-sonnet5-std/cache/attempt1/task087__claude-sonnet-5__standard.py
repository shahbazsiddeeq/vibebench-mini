def parse_cookie(header):
    result = {}
    if not header:
        return result
    for part in header.split(';'):
        if '=' not in part:
            continue
        key, value = part.split('=', 1)
        result[key.strip()] = value.strip()
    return result
