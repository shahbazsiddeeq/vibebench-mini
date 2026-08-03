"""
Module: src.solution

Provides `parse_query_string`, a safe parser for URL query strings
(without a leading '?'), following application/x-www-form-urlencoded
decoding rules.

Security notes:
- Uses only the standard library (urllib.parse.unquote_plus).
- No eval/exec, no dynamic code execution.
- Handles malformed input gracefully (unquote_plus never raises on
  malformed percent-escapes; they are left as-is).
- Enforces strict input type validation to avoid unexpected behavior
  or exceptions leaking internal details.
"""

from urllib.parse import unquote_plus


def parse_query_string(qs: str) -> dict[str, list[str]]:
    """
    Parse a URL query string (without leading '?') into a dict mapping
    each decoded key to an ordered list of its decoded values.

    Rules:
    - Pairs are separated by '&'.
    - Within a pair, key and value are split on the FIRST '=' only.
    - A segment with no '=' becomes that key with value ''.
    - A segment like 'a=' yields value ''.
    - Empty segments (from leading/trailing/doubled '&') are skipped.
    - Both keys and values are percent-decoded; '+' decodes to space.
    - Repeated keys accumulate values in order (never overwritten).
    - Keys are case-sensitive.

    Args:
        qs: The query string to parse.

    Returns:
        A dict[str, list[str]] mapping decoded keys to lists of decoded
        values, in the order they appear.

    Raises:
        TypeError: If `qs` is not a string.
    """
    if not isinstance(qs, str):
        raise TypeError("qs must be a string")

    result: dict[str, list[str]] = {}

    if qs == "":
        return result

    segments = qs.split("&")

    for segment in segments:
        if segment == "":
            continue

        if "=" in segment:
            raw_key, raw_value = segment.split("=", 1)
        else:
            raw_key, raw_value = segment, ""

        key = unquote_plus(raw_key)
        value = unquote_plus(raw_value)

        if key not in result:
            result[key] = []
        result[key].append(value)

    return result
