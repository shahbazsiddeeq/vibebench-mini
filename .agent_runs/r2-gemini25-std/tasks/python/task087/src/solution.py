def parse_cookie(header: str) -> dict:
    """
    Parses a Cookie header string of the form "key=value; key2=value2" into a dict.

    Rules:
      - Split cookie pairs on ';'; split each pair on the FIRST '=' only, so a value may
        itself contain '=' (e.g. base64 values with '=' padding are preserved intact).
      - Surrounding whitespace around keys and values is trimmed.
      - Segments with no '=' are ignored.
      - For duplicate keys, the last value wins.

    Example: parse_cookie("session=abc; user=alice") -> {"session": "abc", "user": "alice"}
    """
    cookies = {}
    if not header:
        return cookies

    pairs = header.split(';')
    for pair in pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()
            cookies[key] = value
    return cookies
