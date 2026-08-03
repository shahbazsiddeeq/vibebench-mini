from __future__ import annotations

import ast


def _parse(source: str) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid Python source: {exc}") from exc


def find_duplicate_dict_keys(source: str) -> list[tuple[int, object]]:
    tree = _parse(source)
    results: list[tuple[int, object]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        seen: set[tuple[str, object]] = set()
        reported: set[tuple[str, object]] = set()
        for key in node.keys:
            if key is None:  # dict unpacking, e.g. {**other}
                continue
            if not isinstance(key, ast.Constant):
                continue
            norm = (type(key.value).__name__, key.value)
            if norm in seen and norm not in reported:
                results.append((node.lineno, key.value))
                reported.add(norm)
            seen.add(norm)

    results.sort(key=lambda t: (t[0], repr(t[1])))
    return results
