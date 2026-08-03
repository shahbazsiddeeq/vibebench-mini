"""
Bare Except Clause Finder.

This module provides a single function, ``find_bare_excepts``, which parses
a string of Python source code using the ``ast`` module and returns the
sorted list of 1-based line numbers of every bare ``except:`` clause.

Only the standard library is used. No use of ``eval``/``exec``. Input is
strictly validated and any parsing failure is surfaced as a ``ValueError``
without leaking internal exception details.
"""

import ast
from typing import List


def find_bare_excepts(source: str) -> List[int]:
    """
    Parse ``source`` as Python code and return the sorted list of 1-based
    line numbers of every bare ``except:`` clause (an ``ast.ExceptHandler``
    whose ``type`` attribute is ``None``).

    :param source: A string containing Python source code.
    :return: Sorted ascending list of line numbers of bare except handlers.
    :raises ValueError: If ``source`` is not a string, or is not valid
        Python source code.
    """
    if not isinstance(source, str):
        raise ValueError("source must be a string")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError("source is not valid Python") from exc
    except (ValueError, TypeError) as exc:
        # ast.parse can raise ValueError for null bytes, etc.
        raise ValueError("source is not valid Python") from exc

    line_numbers: List[int] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            lineno = getattr(node, "lineno", None)
            if isinstance(lineno, int):
                line_numbers.append(lineno)

    return sorted(line_numbers)
