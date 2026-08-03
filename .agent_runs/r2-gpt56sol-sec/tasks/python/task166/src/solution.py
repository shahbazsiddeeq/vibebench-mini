from urllib.parse import unquote_plus


def parse_query_string(qs: str) -> dict[str, list[str]]:
    """Parse an application/x-www-form-urlencoded query string."""
    if not isinstance(qs, str):
        raise TypeError("qs must be a string")

    result: dict[str, list[str]] = {}

    for segment in qs.split("&"):
        if not segment:
            continue

        if "=" in segment:
            raw_key, raw_value = segment.split("=", 1)
        else:
            raw_key, raw_value = segment, ""

        key = unquote_plus(raw_key)
        value = unquote_plus(raw_value)
        result.setdefault(key, []).append(value)

    return result
