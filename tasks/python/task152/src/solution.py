import re

_KEY_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*$")
_UNESCAPE = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"'}


def parse_dotenv(path: str) -> dict[str, str]:
    """Parse a .env file into a dict of string keys and values."""
    result: dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):].lstrip()

            if "=" not in line:
                raise ValueError(f"missing '=' in line: {raw_line!r}")

            key, raw_value = line.split("=", 1)
            key = key.strip()
            if not _KEY_RE.match(key):
                raise ValueError(f"invalid key: {key!r}")

            result[key] = _parse_value(raw_value)
    return result


def _parse_value(raw: str) -> str:
    if len(raw) >= 2 and raw[0] == '"' and raw[-1] == '"':
        return _unescape(raw[1:-1])
    if len(raw) >= 2 and raw[0] == "'" and raw[-1] == "'":
        return raw[1:-1]
    return _strip_inline_comment(raw).strip()


def _strip_inline_comment(raw: str) -> str:
    for i, ch in enumerate(raw):
        if ch == "#" and (i == 0 or raw[i - 1].isspace()):
            return raw[:i]
    return raw


def _unescape(s: str) -> str:
    out: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] in _UNESCAPE:
            out.append(_UNESCAPE[s[i + 1]])
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)
