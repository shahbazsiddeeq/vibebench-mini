from collections.abc import Mapping
from typing import Any


def expand_cases(
    base: Mapping[Any, Any],
    overrides: list[Mapping[Any, Any]],
) -> list[dict[Any, Any]]:
    """Return shallow copies of base, each updated by one override."""
    return [{**base, **override} for override in overrides]
