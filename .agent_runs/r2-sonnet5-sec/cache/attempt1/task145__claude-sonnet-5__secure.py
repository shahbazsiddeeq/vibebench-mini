"""
src/solution.py

A small, safe template-rendering utility.

render_template(template, values) -> str

Rules:
    * "{{" -> literal "{"
    * "}}" -> literal "}"
    * "{name}" where name matches [A-Za-z0-9_]+ -> str(values[name])
    * Any other appearance of "{" or "}" is an error.
    * Missing key for a valid placeholder raises KeyError(name).
    * Malformed placeholder (empty, illegal chars, unterminated) raises ValueError.
    * All other characters (including non-ASCII) are copied verbatim.

This implementation performs a strict, single-pass, left-to-right scan
and does not use eval/exec or any external data sources.
"""

import re
from typing import Any, Dict

_NAME_RE = re.compile(r'^[A-Za-z0-9_]+$')


def render_template(template: str, values: Dict[str, Any]) -> str:
    """Render a template string by substituting placeholders with values.

    Args:
        template: The template string containing placeholders like "{name}",
                   plus escaped braces "{{" and "}}".
        values: A mapping from placeholder names to substitution values.

    Returns:
        The rendered string.

    Raises:
        TypeError: If `template` is not a str or `values` is not a mapping.
        ValueError: If a brace is malformed (unescaped stray brace, empty
                    placeholder, illegal characters in a name, or an
                    unterminated placeholder).
        KeyError: If a valid placeholder's name is not present in `values`.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    if not isinstance(values, dict):
        raise TypeError("values must be a dict")

    n = len(template)
    result = []
    i = 0

    while i < n:
        ch = template[i]

        if ch == '{':
            # Escaped '{{' -> literal '{'
            if i + 1 < n and template[i + 1] == '{':
                result.append('{')
                i += 2
                continue

            # Otherwise, must be a placeholder "{name}"
            j = i + 1
            start = j
            while j < n and template[j] != '}':
                j += 1

            if j >= n:
                # No closing brace found -> unterminated placeholder
                raise ValueError(
                    "Unterminated placeholder starting at position %d" % i
                )

            name = template[start:j]

            if not _NAME_RE.match(name):
                raise ValueError(
                    "Invalid placeholder name %r at position %d" % (name, i)
                )

            if name not in values:
                raise KeyError(name)

            result.append(str(values[name]))
            i = j + 1
            continue

        elif ch == '}':
            # Escaped '}}' -> literal '}'
            if i + 1 < n and template[i + 1] == '}':
                result.append('}')
                i += 2
                continue
            else:
                raise ValueError(
                    "Unmatched '}' at position %d" % i
                )

        else:
            result.append(ch)
            i += 1

    return ''.join(result)
