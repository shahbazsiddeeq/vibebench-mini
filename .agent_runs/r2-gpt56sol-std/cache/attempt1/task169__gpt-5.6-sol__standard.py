"""Utilities for parsing HTTP Accept-Language headers."""

import re


_Q_VALUE_RE = re.compile(r"(?:0(?:\.\d{1,3})?|1(?:\.0{1,3})?)\Z")


def parse_accept_language(value: str) -> list[tuple[str, float]]:
    """Parse an Accept-Language header into quality-sorted language pairs."""
    result: list[tuple[str, float]] = []

    for raw_entry in value.split(","):
        entry = raw_entry.strip()
        if not entry:
            continue

        segments = entry.split(";")
        if len(segments) > 2:
            raise ValueError("an entry may contain at most one parameter")

        language_tag = segments[0].strip()
        if not language_tag:
            raise ValueError("language tag cannot be empty")

        quality = 1.0

        if len(segments) == 2:
            parameter = segments[1].strip()
            if "=" not in parameter:
                raise ValueError("malformed q-parameter")

            key, q_value = parameter.split("=", 1)
            if key.lower() != "q" or not q_value or not _Q_VALUE_RE.fullmatch(q_value):
                raise ValueError("invalid q-parameter")

            quality = float(q_value)

        if quality != 0.0:
            result.append((language_tag.lower(), quality))

    result.sort(key=lambda item: item[1], reverse=True)
    return result
