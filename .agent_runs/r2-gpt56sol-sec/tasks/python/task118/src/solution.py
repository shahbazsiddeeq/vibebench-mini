"""Utilities for flattening nested dictionaries."""

from typing import Any


def flatten_dict(d: dict[str, Any], sep: str = ".") -> dict[str, Any]:
    """
    Flatten a nested dictionary by joining string keys with ``sep``.

    Non-dictionary values and empty dictionaries are treated as leaves.
    A ValueError is raised if distinct paths produce the same flattened key
    or if a dictionary contains a cycle.
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dictionary")
    if not isinstance(sep, str):
        raise TypeError("sep must be a string")
    if not d:
        return {}

    result: dict[str, Any] = {}
    active: set[int] = set()
    stack: list[tuple[str, Any, tuple[str, ...]]] = [("visit", d, ())]

    while stack:
        action, value, path = stack.pop()

        if action == "exit":
            active.remove(id(value))
            continue

        value_id = id(value)
        if value_id in active:
            raise ValueError("cyclic dictionaries cannot be flattened")

        active.add(value_id)
        stack.append(("exit", value, path))

        items = list(dict.items(value))
        for key, child in reversed(items):
            if not isinstance(key, str):
                raise TypeError("dictionary keys must be strings")

            child_path = path + (key,)

            if isinstance(child, dict) and child:
                stack.append(("visit", child, child_path))
                continue

            flat_key = sep.join(child_path)
            if flat_key in result:
                raise ValueError("separator collision in flattened keys")
            result[flat_key] = child

    return result
