"""
src/solution.py

A small, self-contained .env file parser.
"""

import os
import re

_KEY_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def _unescape_double_quoted(s: str) -> str:
    """Unescape \\n, \\t, \\r, \\\\ and \\" inside a double-quoted value."""
    result = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '\\' and i + 1 < n:
            nxt = s[i + 1]
            if nxt == 'n':
                result.append('\n')
                i += 2
                continue
            elif nxt == 't':
                result.append('\t')
                i += 2
                continue
            elif nxt == 'r':
                result.append('\r')
                i += 2
                continue
            elif nxt == '\\':
                result.append('\\')
                i += 2
                continue
            elif nxt == '"':
                result.append('"')
                i += 2
                continue
            else:
                result.append(c)
                i += 1
                continue
        else:
            result.append(c)
            i += 1
    return ''.join(result)


def _strip_inline_comment(s: str) -> str:
    """Strip an inline comment: '#' at index 0 or preceded by whitespace."""
    for idx, ch in enumerate(s):
        if ch == '#':
            if idx == 0 or s[idx - 1].isspace():
                return s[:idx]
    return s


def parse_dotenv(path: str) -> dict:
    """Parse a .env file into a dict of key -> value."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file: {path}")

    result = {}

    with open(path, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line or line.startswith('#'):
                continue

            if line.startswith('export '):
                line = line[len('export '):]

            if '=' not in line:
                raise ValueError(f"Invalid line (no '='): {raw_line!r}")

            key_part, value_part = line.split('=', 1)
            key = key_part.strip()

            if not key or not _KEY_RE.match(key):
                raise ValueError(f"Invalid key: {key!r}")

            if len(value_part) >= 2 and value_part.startswith('"') and value_part.endswith('"'):
                inner = value_part[1:-1]
                value = _unescape_double_quoted(inner)
            elif len(value_part) >= 2 and value_part.startswith("'") and value_part.endswith("'"):
                value = value_part[1:-1]
            else:
                stripped_comment = _strip_inline_comment(value_part)
                value = stripped_comment.strip()

            result[key] = value

    return result
