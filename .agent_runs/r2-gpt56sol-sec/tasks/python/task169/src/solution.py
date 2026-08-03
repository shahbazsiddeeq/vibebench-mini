"""Utilities for parsing HTTP Accept-Language headers."""

from __future__ import annotations

import re


_Q_VALUE_PATTERN = re.compile(r"(?:0(?:\.\d{1,3})?|1(?:\.0{1,3})?)\Z")


def parse_accept_language(value: str) -> list[tuple[str, float]]:
    """Parse an Accept-Language header into quality-sorted language pairs.

    Empty comma-separated entries are ignored. Invalid entries or quality
    parameters raise ValueError.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    parsed: list[tuple[str, float]] = []

    for raw_entry in value.split(","):
        entry = raw_entry.strip()
        if not entry:
            continue

        segments = entry.split(";")
        if len(segments) > 2:
            raise ValueError("entry contains more than one parameter segment")

        language_tag = segments[0].strip()
        if not language_tag:
            raise ValueError("language tag must not be empty")

        quality = 1.0

        if len(segments) == 2:
            parameter = segments[1].strip()
            if parameter.count("=") != 1:
                raise ValueError("malformed q-parameter")

            key, raw_quality = (part.strip() for part in parameter.split("=", 1))
            if key.lower() != "q":
                raise ValueError("unknown parameter")
            if not _Q_VALUE_PATTERN.fullmatch(raw_quality):
                raise ValueError("invalid quality value")

            quality = float(raw_quality)

        if quality > 0.0:
            parsed.append((language_tag.lower(), quality))

    parsed.sort(key=lambda item: item[1], reverse=True)
    return parsed
