"""
Accept-Language header parser.

Provides parse_accept_language(value: str) -> list[tuple[str, float]]

This implementation avoids eval/exec, does not use randomness, and treats
the incoming header value as untrusted external data: it is validated
strictly and any deviation from the expected grammar raises ValueError
without leaking internal state.
"""

from __future__ import annotations

import re
from typing import List, Tuple

# Matches a valid q-value: 0, 0.x, 0.xx, 0.xxx, 1, 1.0, 1.00, 1.000
_Q_VALUE_RE = re.compile(r"^(0(\.\d{1,3})?|1(\.0{1,3})?)$")


def _parse_q(raw_q: str) -> float:
    """Validate and convert a q-value string to a float in [0, 1]."""
    raw_q = raw_q.strip()
    if not _Q_VALUE_RE.match(raw_q):
        raise ValueError("Invalid q-value in Accept-Language header")
    try:
        q = float(raw_q)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid q-value in Accept-Language header") from exc
    if not (0.0 <= q <= 1.0):
        raise ValueError("q-value out of range in Accept-Language header")
    return q


def _parse_entry(entry: str) -> Tuple[str, float]:
    """Parse a single 'lang-range[;q=weight]' entry."""
    segments = entry.split(";")

    if len(segments) > 2:
        raise ValueError("Malformed Accept-Language entry: too many ';' segments")

    tag = segments[0].strip().lower()
    if not tag:
        raise ValueError("Empty language tag in Accept-Language header")

    if len(segments) == 1:
        return tag, 1.0

    param = segments[1].strip()
    if not param:
        raise ValueError("Malformed q-parameter in Accept-Language header")

    if param.count("=") != 1:
        raise ValueError("Malformed q-parameter in Accept-Language header")

    key, _, raw_value = param.partition("=")
    key = key.strip().lower()
    if key != "q":
        raise ValueError(f"Unknown parameter '{key}' in Accept-Language header")

    quality = _parse_q(raw_value)
    return tag, quality


def parse_accept_language(value: str) -> List[Tuple[str, float]]:
    """
    Parse an HTTP Accept-Language header value into a list of
    (language_tag, quality) tuples, sorted by quality descending
    (stable: ties preserve original left-to-right order).

    Entries with q=0 are dropped. Raises ValueError on malformed input.
    """
    if not isinstance(value, str):
        raise ValueError("Accept-Language header value must be a string")

    if not value.strip():
        return []

    results: List[Tuple[str, float]] = []

    for raw_entry in value.split(","):
        entry = raw_entry.strip()
        if not entry:
            # Skip empty entries from doubled or trailing commas.
            continue

        tag, quality = _parse_entry(entry)

        if quality == 0.0:
            continue

        results.append((tag, quality))

    # Stable sort by quality descending; ties keep original order.
    results.sort(key=lambda pair: -pair[1])

    return results
