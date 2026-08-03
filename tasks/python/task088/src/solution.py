from __future__ import annotations


def parse_email_headers(raw: str) -> dict[str, str]:
    result: dict[str, str] = {}
    current_key: str | None = None
    current_val: list[str] = []
    for line in raw.splitlines():
        if line and line[0] in (" ", "\t"):
            if current_key is not None:
                current_val.append(line.strip())
        elif ":" in line:
            if current_key is not None:
                result[current_key] = " ".join(current_val)
            k, _, v = line.partition(":")
            current_key = k.strip().title()
            current_val = [v.strip()]
        elif not line.strip():
            break
    if current_key is not None:
        result[current_key] = " ".join(current_val)
    return result
