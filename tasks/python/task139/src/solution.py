from __future__ import annotations

from typing import Any


def expand_cases(base: dict, overrides: list[dict]) -> list[dict]:
    """Expand ``base`` into one new dict per override.

    Each result is base merged with a single override (override values win).
    ``base`` is never mutated. An empty ``overrides`` yields an empty list.
    """
    result: list[dict[Any, Any]] = []
    for override in overrides:
        merged = dict(base)
        merged.update(override)
        result.append(merged)
    return result
