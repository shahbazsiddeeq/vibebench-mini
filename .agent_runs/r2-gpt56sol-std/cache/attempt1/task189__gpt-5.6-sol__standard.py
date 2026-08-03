import ast
from typing import Any


__all__ = ["find_duplicate_dict_keys"]


_ALLOWED_CONSTANT_TYPES = (int, float, complex, str, bytes, bool, type(None))


def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    """Return type-sensitive duplicate constant keys from each dict literal."""
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(str(exc)) from exc

    duplicates: list[tuple[int, object]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue

        seen: list[Any] = []
        reported: list[Any] = []

        for key_node in node.keys:
            if not isinstance(key_node, ast.Constant):
                continue

            value = key_node.value
            if type(value) not in _ALLOWED_CONSTANT_TYPES:
                continue

            matching_seen = next(
                (
                    existing
                    for existing in seen
                    if type(existing) is type(value) and existing == value
                ),
                None,
            )

            if matching_seen is None:
                seen.append(value)
                continue

            already_reported = any(
                type(existing) is type(value) and existing == value
                for existing in reported
            )
            if not already_reported:
                reported.append(matching_seen)
                duplicates.append((node.lineno, matching_seen))

    duplicates.sort(key=lambda item: (item[0], repr(item[1])))
    return duplicates
