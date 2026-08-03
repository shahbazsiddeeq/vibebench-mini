from __future__ import annotations

import ast


def _parse(source: str) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid Python source: {exc}") from exc


def find_bare_excepts(source: str) -> list[int]:
    """Return sorted line numbers of bare ``except:`` handlers."""
    tree = _parse(source)
    lines: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            lines.append(node.lineno)
    return sorted(lines)
