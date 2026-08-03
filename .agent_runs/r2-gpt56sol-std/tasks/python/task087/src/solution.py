def parse_cookie(header: str) -> dict[str, str]:
    cookies: dict[str, str] = {}

    for segment in header.split(";"):
        if "=" not in segment:
            continue
        key, value = segment.split("=", 1)
        cookies[key.strip()] = value.strip()

    return cookies
