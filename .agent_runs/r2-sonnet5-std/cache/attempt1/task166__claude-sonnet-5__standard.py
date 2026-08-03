"""Parse URL query string into a dict of lists."""
from urllib.parse import unquote_plus


def parse_query_string(qs: str) -> dict:
    result: dict = {}
    if not qs:
        return result
    for segment in qs.split('&'):
        if not segment:
            continue
        if '=' in segment:
            key, value = segment.split('=', 1)
        else:
            key, value = segment, ''
        key = unquote_plus(key)
        value = unquote_plus(value)
        result.setdefault(key, []).append(value)
    return result
