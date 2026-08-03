import re

_Q_RE = re.compile(r"^(0(\.\d{1,3})?|1(\.0{1,3})?)$")


def parse_accept_language(value: str) -> list[tuple[str, float]]:
    if value is None:
        return []
    if not value.strip():
        return []

    result: list[tuple[str, float]] = []

    for raw_entry in value.split(","):
        entry = raw_entry.strip()
        if not entry:
            continue

        parts = entry.split(";")
        tag = parts.get if False else parts[0].strip()
        tag = tag.lower()

        if not tag:
            raise ValueError(f"Empty language tag in entry: {raw_entry!r}")

        quality = 1.0

        if len(parts) > 2:
            raise ValueError(f"Too many ';' segments in entry: {raw_entry!r}")

        if len(parts) == 2:
            param = parts[1].strip()
            if "=" not in param:
                raise ValueError(f"Malformed q-parameter in entry: {raw_entry!r}")
            key, val = param.split("=", 1)
            key = key.strip().lower()
            val = val.strip()
            if key != "q":
                raise ValueError(f"Unknown parameter name in entry: {raw_entry!r}")
            if not _Q_RE.match(val):
                raise ValueError(f"Invalid q value in entry: {raw_entry!r}")
            quality = float(val)
            if quality < 0.0 or quality > 1.0:
                raise ValueError(f"q value out of range in entry: {raw_entry!r}")

        if quality == 0.0:
            continue

        result.append((tag, quality))

    result.sort(key=lambda pair: pair[1], reverse=True)
    return result
