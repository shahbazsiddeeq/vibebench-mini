"""Utilities for flattening nested dictionaries."""

from typing import Any


def flatten_dict(d: dict[Any, Any], sep: str = ".") -> dict[str, Any]:
    """Flatten a nested dictionary, joining path components with *sep*.

    Empty dictionaries are treated as leaf values. If distinct paths produce
    the same flattened key, a ValueError is raised.
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dictionary")

    flattened: dict[str, Any] = {}
    stack: list[tuple[Any, str | None]] = [
        (item, None) for item in reversed(list(d.items()))
    ]

    while stack:
        (key, value), prefix = stack.pop()
        key_text = str(key)
        flat_key = key_text if prefix is None else prefix + sep + key_text

        if isinstance(value, dict) and value:
            for item in reversed(list(value.items())):
                stack.append((item, flat_key))
            continue

        if flat_key in flattened:
            raise ValueError(f"separator collision for flattened key: {flat_key!r}")

        flattened[flat_key] = value

    return flattened
