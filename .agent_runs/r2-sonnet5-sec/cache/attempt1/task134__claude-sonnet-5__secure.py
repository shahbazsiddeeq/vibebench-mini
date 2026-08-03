"""
Module: solution.py

Provides `non_snake_case_functions(source)` which parses Python source code
and returns the names of all function/method definitions (including nested
functions and async functions) whose names do not conform to snake_case
convention: ^[a-z_][a-z0-9_]*$

Security notes:
- Uses `ast.parse` only (no eval/exec) to safely parse source into an AST.
- Does not execute any code from the provided source.
- Validates input type before processing.
- Catches SyntaxError and other parsing-related exceptions, raising a
  generic ValueError without leaking internal exception details.
"""

import ast
import re
from typing import List

_SNAKE_CASE_RE = re.compile(r"^[a-z_][a-z0-9_]*$")


def non_snake_case_functions(source: str) -> List[str]:
    """
    Parse `source` and return the names of all function definitions
    (including nested functions, async functions, and methods) whose
    names do not match snake_case convention.

    Names are returned in source order (by line number, then column).

    Raises:
        ValueError: if `source` is not a string, or cannot be parsed.
    """
    if not isinstance(source, str):
        raise ValueError("source must be a string")

    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        raise ValueError("invalid source: could not parse")
    except Exception:
        # Avoid leaking any internal exception details.
        raise ValueError("invalid source: could not parse")

    matches = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            if not isinstance(name, str):
                continue
            if not _SNAKE_CASE_RE.match(name):
                lineno = getattr(node, "lineno", 0)
                col_offset = getattr(node, "col_offset", 0)
                matches.append((lineno, col_offset, name))

    matches.sort(key=lambda t: (t[0], t[1]))

    return [name for (_, _, name) in matches]
