import ast
from typing import Any


def _is_supported_constant(value: object) -> bool:
    return value is None or type(value) in (bool, int, float, complex, str, bytes)


def _same_typed_value(left: object, right: object) -> bool:
    return type(left) is type(right) and left == right


def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc

    results: list[tuple[int, object]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue

        seen: list[Any] = []
        duplicates: list[Any] = []

        for key_node in node.keys:
            if key_node is None or not isinstance(key_node, ast.Constant):
                continue

            value = key_node.value
            if not _is_supported_constant(value):
                continue

            if any(_same_typed_value(value, prior) for prior in seen):
                if not any(_same_typed_value(value, prior) for prior in duplicates):
                    duplicates.append(value)
            else:
                seen.append(value)

        results.extend((node.lineno, value) for value in duplicates)

    results.sort(key=lambda item: (item[0], repr(item[1])))
    return results
