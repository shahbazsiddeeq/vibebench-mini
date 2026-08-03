"""
Deep Dict Merge
===============

Provides ``deep_merge(base, override)`` which recursively merges two
dictionaries. Values from ``override`` take precedence over values from
``base``. When both sides have a dict for the same key, they are merged
recursively; otherwise the ``override`` value replaces the ``base`` value
entirely (no concatenation of lists, no partial merging of other types).

The function never mutates its inputs and returns a brand new top-level
dict. Nested dict values that are taken unchanged from ``base`` (i.e. keys
that only exist in ``base`` or whose ``override`` counterpart is not a
dict while the base value is, etc.) are referenced as-is (not deep-copied)
to match the documented behaviour.
"""

from typing import Any, Dict

__all__ = ["deep_merge"]


def _validate_dict(value: Any, name: str) -> None:
    """Raise a TypeError with a safe, generic message if *value* is not a dict."""
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict")


def deep_merge(base: Dict[Any, Any], override: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge ``override`` into ``base`` without mutating either.

    Rules:
      * If a key exists only in one dict, its value is used as-is.
      * If a key exists in both and both values are dicts, they are merged
        recursively.
      * If a key exists in both but either value is not a dict, the value
        from ``override`` replaces the one from ``base`` outright (lists
        are not concatenated, scalars are simply overwritten).

    Args:
        base: The base dictionary.
        override: The dictionary whose values take precedence.

    Returns:
        A new dictionary representing the merged result. Neither ``base``
        nor ``override`` is modified.

    Raises:
        TypeError: If either argument is not a dict.
    """
    _validate_dict(base, "base")
    _validate_dict(override, "override")

    result: Dict[Any, Any] = {}

    for key, value in base.items():
        result[key] = value

    for key, override_value in override.items():
        if key in result:
            base_value = result[key]
            if isinstance(base_value, dict) and isinstance(override_value, dict):
                result[key] = deep_merge(base_value, override_value)
            else:
                result[key] = override_value
        else:
            result[key] = override_value

    return result
