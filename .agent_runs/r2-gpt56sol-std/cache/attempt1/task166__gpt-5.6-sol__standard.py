from urllib.parse import unquote_plus


def parse_query_string(qs: str) -> dict[str, list[str]]:
    """Parse a URL query string into decoded keys and ordered value lists."""
    result: dict[str, list[str]] = {}

    for segment in qs.split("&"):
        if not segment:
            continue

        key, separator, value = segment.partition("=")
        if not separator:
            value = ""

        decoded_key = unquote_plus(key)
        decoded_value = unquote_plus(value)
        result.setdefault(decoded_key, []).append(decoded_value)

    return result
