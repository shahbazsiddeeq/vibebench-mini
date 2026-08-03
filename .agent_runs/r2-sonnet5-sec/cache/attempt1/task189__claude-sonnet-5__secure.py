import ast
from typing import Any


def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    if not isinstance(source, str):
        raise ValueError("source must be a string")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python source: {exc}") from exc
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Invalid Python source: {exc}") from exc

    results: list[tuple[int, Any]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue

        seen_count: dict[tuple[type, Any], int] = {}
        seen_value: dict[tuple[type, Any], Any] = {}

        for key_node in node.keys:
            if key_node is None:
                continue
            if type(key_node) is not ast.Constant:
                continue

            value = key_node.value
            type_key = (type(value), value)

            seen_count[type_key] = seen_count.get(type_key, 0) + 1
            seen_value[type_key] = value

        for type_key, count in seen_count.items():
            if count > 1:
                results.append((node.lineno, seen_value[type_key]))

    results.sort(key=lambda item: (item[0], repr(item[1])))
    return results
