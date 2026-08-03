import re

_UNITS = {'w': 604800, 'd': 86400, 'h': 3600, 'm': 60, 's': 1}
_SEGMENT_RE = re.compile(r'(\d+)([wdhms])')
_FULL_RE = re.compile(r'(?:\d+[wdhms])+')


def parse_duration(text: str) -> int:
    if not isinstance(text, str) or not _FULL_RE.fullmatch(text):
        raise ValueError(f"Invalid duration string: {text!r}")

    total = 0
    for number, unit in _SEGMENT_RE.findall(text):
        total += int(number) * _UNITS[unit]
    return total
