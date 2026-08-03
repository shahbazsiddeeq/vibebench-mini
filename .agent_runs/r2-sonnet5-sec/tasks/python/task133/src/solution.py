"""
Module: solution

Provides docstring_coverage(source): parses Python source code and
computes the fraction of function/class definitions that contain a
docstring.

Security notes:
- Uses `ast.parse` only (no eval/exec) so untrusted source text is
  never executed, only statically analyzed.
- Validates input type before processing.
- Catches parsing errors (SyntaxError, ValueError) and re-raises as
  ValueError with a sanitized, generic message (no internal details
  or file paths leaked).
"""

import ast
from typing import Union


def docstring_coverage(source: str) -> float:
    """
    Compute the fraction of function and class definitions in `source`
    that have a docstring.

    Args:
        source: Python source code as a string.

    Returns:
        A float between 0.0 and 1.0 representing the fraction of
        FunctionDef/AsyncFunctionDef/ClassDef nodes that have a
        docstring. Returns 1.0 if there are no such definitions.

    Raises:
        ValueError: If `source` is not a string or cannot be parsed
            as valid Python source.
    """
    if not isinstance(source, str):
        raise ValueError("Invalid source: expected a string")

    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        raise ValueError("Invalid source: could not parse as Python code")
    except Exception:
        # Defensive: never leak internal exception details.
        raise ValueError("Invalid source: could not parse as Python code")

    definitions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.append(node)

    if not definitions:
        return 1.0

    documented = 0
    for node in definitions:
        try:
            doc = ast.get_docstring(node)
        except Exception:
            doc = None
        if doc is not None:
            documented += 1

    return documented / len(definitions)
