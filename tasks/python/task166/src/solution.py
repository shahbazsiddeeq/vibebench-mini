from urllib.parse import unquote_plus


def parse_query_string(qs: str) -> dict[str, list[str]]:
    """Parse a URL query string into a dict of key -> list of values.

    The input must NOT include a leading '?'. Pairs are split on '&';
    empty segments are skipped. Each pair splits on the first '=' only;
    a segment without '=' maps the key to ''. Keys and values are
    decoded with application/x-www-form-urlencoded rules ('+' -> space,
    percent-decoding). Repeated keys accumulate their values in order.
    """
    if not isinstance(qs, str):
        raise ValueError("qs must be a string")
    result: dict[str, list[str]] = {}
    for segment in qs.split("&"):
        if segment == "":
            continue
        if "=" in segment:
            raw_key, raw_value = segment.split("=", 1)
        else:
            raw_key, raw_value = segment, ""
        key = unquote_plus(raw_key)
        value = unquote_plus(raw_value)
        result.setdefault(key, []).append(value)
    return result
