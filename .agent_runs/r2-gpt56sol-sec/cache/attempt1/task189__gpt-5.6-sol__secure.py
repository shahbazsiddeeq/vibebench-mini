import ast
from typing import Any

__all__ = ["find_duplicate_dict_keys"]

_ALLOWED_CONSTANT_TYPES = (int, float, complex, str, bytes, bool, type(None))


def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    """Return duplicate constant keys found in each dictionary display."""
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        raise ValueError("source is not valid Python") from None

    duplicates: list[tuple[int, object]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue

        representatives: list[Any] = []
        reported: list[bool] = []

        for key_node in node.keys:
            if key_node is None or not isinstance(key_node, ast.Constant):
                continue

            value = key_node.value
            if type(value) not in _ALLOWED_CONSTANT_TYPES:
                continue

            match_index = None
            for index, existing in enumerate(representatives):
                if type(value) is type(existing) and value == existing:
                    match_index = index
                    break

            if match_index is None:
                representatives.append(value)
                reported.append(False)
            elif not reported[match_index]:
                duplicates.append((node.lineno, representatives[match_index]))
                reported[match_index] = True

    duplicates.sort(key=lambda item: (item[0], repr(item[1])))
    return duplicates
