"""Utilities for recursively merging dictionaries."""

from typing import Any


def deep_merge(base: dict[Any, Any], override: dict[Any, Any]) -> dict[Any, Any]:
    """Return a recursive merge of two dictionaries.

    Values from ``override`` take precedence. When values for the same key are
    both dictionaries, they are recursively merged. All other conflicts are
    resolved by using the override value.

    Neither input is modified. Nested values that do not require merging are
    shared with their respective input dictionaries.
    """
    if not isinstance(base, dict):
        raise TypeError("base must be a dictionary")
    if not isinstance(override, dict):
        raise TypeError("override must be a dictionary")

    result = base.copy()

    for key, override_value in override.items():
        base_value = base.get(key)
        if key in base and isinstance(base_value, dict) and isinstance(
            override_value, dict
        ):
            result[key] = deep_merge(base_value, override_value)
        else:
            result[key] = override_value

    return result
