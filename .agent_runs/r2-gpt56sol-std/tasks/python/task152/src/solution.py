import re


_KEY_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_ESCAPES = {
    "n": "\n",
    "t": "\t",
    "r": "\r",
    "\\": "\\",
    '"': '"',
}


def _unescape_double_quoted(value: str) -> str:
    result: list[str] = []
    index = 0

    while index < len(value):
        char = value[index]
        if char == "\\" and index + 1 < len(value):
            escaped = value[index + 1]
            if escaped in _ESCAPES:
                result.append(_ESCAPES[escaped])
                index += 2
                continue
        result.append(char)
        index += 1

    return "".join(result)


def _parse_value(raw_value: str) -> str:
    if len(raw_value) >= 2 and raw_value.startswith('"') and raw_value.endswith('"'):
        return _unescape_double_quoted(raw_value[1:-1])

    if len(raw_value) >= 2 and raw_value.startswith("'") and raw_value.endswith("'"):
        return raw_value[1:-1]

    for index, char in enumerate(raw_value):
        if char == "#" and (index == 0 or raw_value[index - 1].isspace()):
            raw_value = raw_value[:index]
            break

    return raw_value.strip()


def parse_dotenv(path: str) -> dict[str, str]:
    result: dict[str, str] = {}

    with open(path, "r", encoding="utf-8") as dotenv_file:
        for line in dotenv_file:
            text = line.strip()

            if not text or text.startswith("#"):
                continue

            if text.startswith("export "):
                text = text[len("export "):]

            if "=" not in text:
                raise ValueError(f"Invalid dotenv line: {text!r}")

            key, raw_value = text.split("=", 1)
            key = key.strip()

            if not key or _KEY_PATTERN.fullmatch(key) is None:
                raise ValueError(f"Invalid dotenv key: {key!r}")

            result[key] = _parse_value(raw_value)

    return result
