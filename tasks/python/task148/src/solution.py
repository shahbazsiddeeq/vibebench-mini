import re

_UNITS = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
_SEGMENT = re.compile(r"([0-9]+)([wdhms])")
_FULL = re.compile(r"(?:[0-9]+[wdhms])+")


def parse_duration(text: str) -> int:
    """Parse a compact duration string like '1h30m' into total seconds."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not _FULL.fullmatch(text):
        raise ValueError(f"invalid duration string: {text!r}")
    total = 0
    for value, unit in _SEGMENT.findall(text):
        total += int(value) * _UNITS[unit]
    return total
