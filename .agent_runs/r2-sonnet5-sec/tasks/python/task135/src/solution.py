"""Unused Import Detector.

Provides `unused_imports(source)` which statically analyzes Python source
code using the `ast` module to determine which imported names are never
referenced elsewhere in the code as a real `ast.Name` node.
"""

import ast
from typing import List


def unused_imports(source: str) -> List[str]:
    """Return the list of imported names that are never used.

    A name introduced via `import x`, `import x as y`, `import a.b.c`
    (binds `a`), or `from mod import x` / `from mod import x as y` is
    considered "used" only if it appears as an `ast.Name` node elsewhere
    in the source. Names appearing inside string literals or comments do
    not count as usage. Star imports (`from m import *`) bind no
    inspectable name and are never reported.

    Args:
        source: The Python source code to analyze.

    Returns:
        A list of unused import binding names, in the order they were
        first bound in the source.

    Raises:
        ValueError: If the source cannot be parsed due to a syntax error.
    """
    if not isinstance(source, str):
        raise ValueError("source must be a string")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"invalid syntax: {exc}") from None
    except ValueError as exc:
        # e.g. null bytes in source
        raise ValueError(f"invalid source: {exc}") from None

    # Collect import bindings in source order, keyed by (lineno, col_offset)
    # to ensure a stable ordering that follows the textual layout.
    bindings = []  # list of (lineno, col_offset, name)
    seen_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound = alias.asname if alias.asname else alias.name.split(".")[0]
                bindings.append((node.lineno, node.col_offset, bound))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    # Star import binds no inspectable name.
                    continue
                bound = alias.asname if alias.asname else alias.name
                bindings.append((node.lineno, node.col_offset, bound))

    # Collect all real Name usages (loads, stores, deletes - any Name node).
    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    # Sort bindings by their source position to preserve source order.
    bindings.sort(key=lambda item: (item[0], item[1]))

    result = []
    for _, _, name in bindings:
        if name not in used_names:
            result.append(name)

    return result
