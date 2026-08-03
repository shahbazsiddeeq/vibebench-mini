"""Utilities for expanding a base test case with individual overrides."""

from collections.abc import Iterable, Mapping
from typing import Any


def expand_cases(
    base: Mapping[Any, Any],
    overrides: Iterable[Mapping[Any, Any]],
) -> list[dict[Any, Any]]:
    """Return shallow copies of *base*, each updated by one override."""
    if not isinstance(base, Mapping):
        raise TypeError("base must be a mapping")
    if isinstance(overrides, (str, bytes, bytearray)) or not isinstance(
        overrides, Iterable
    ):
        raise TypeError("overrides must be an iterable of mappings")

    results: list[dict[Any, Any]] = []
    for override in overrides:
        if not isinstance(override, Mapping):
            raise TypeError("each override must be a mapping")
        expanded = dict(base)
        expanded.update(override)
        results.append(expanded)

    return results
