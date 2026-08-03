"""
Duration string parser.

Parses compact duration strings composed of one or more segments of the
form <non-negative integer><unit>, where unit is one of:
    w = 604800 seconds (week)
    d = 86400 seconds (day)
    h = 3600 seconds (hour)
    m = 60 seconds (minute)
    s = 1 second

Example: "1h30m" -> 5400
"""

import re

# Precompiled pattern for a single segment: one or more ASCII digits
# followed immediately by exactly one lowercase unit letter.
_SEGMENT_RE = re.compile(r'\d+[wdhms]')

# Precompiled pattern to validate the *entire* string consists of one
# or more such segments, with nothing else (no whitespace, signs, etc.).
_FULL_RE = re.compile(r'(?:\d+[wdhms])+')

_UNIT_SECONDS = {
    'w': 604800,
    'd': 86400,
    'h': 3600,
    'm': 60,
    's': 1,
}


def parse_duration(text: str) -> int:
    """
    Convert a compact duration string into a total number of seconds.

    Args:
        text: The duration string, e.g. "1h30m".

    Returns:
        Total number of seconds as an int.

    Raises:
        ValueError: If the input does not fully match the required
            grammar (empty string, missing unit, missing number,
            unknown/uppercase unit, whitespace, decimals, signs, or
            any stray trailing/leading characters).
    """
    if not isinstance(text, str):
        raise ValueError("Duration must be a string")

    if text == "":
        raise ValueError("Duration string must not be empty")

    # Ensure the *whole* string matches the grammar exactly - no partial
    # matches, no leading/trailing junk, no whitespace.
    if _FULL_RE.fullmatch(text) is None:
        raise ValueError("Invalid duration string format")

    total_seconds = 0
    for match in _SEGMENT_RE.finditer(text):
        segment = match.group()
        unit = segment[-1]
        number_part = segment[:-1]
        try:
            value = int(number_part)
        except ValueError:
            # Should not happen given the regex, but guard anyway.
            raise ValueError("Invalid numeric segment in duration string")
        total_seconds += value * _UNIT_SECONDS[unit]

    return total_seconds
