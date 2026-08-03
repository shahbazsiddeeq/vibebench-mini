from __future__ import annotations


def parse_cookie(header: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for part in header.split(";"):
        part = part.strip()
        if "=" in part:
            k, _, v = part.partition("=")
            result[k.strip()] = v.strip()
    return result
