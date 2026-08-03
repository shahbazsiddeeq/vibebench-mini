from __future__ import annotations


def classify_status(code: int) -> str:
    if 100 <= code <= 199:
        return "informational"
    elif 200 <= code <= 299:
        return "success"
    elif 300 <= code <= 399:
        return "redirect"
    elif 400 <= code <= 499:
        return "client_error"
    elif 500 <= code <= 599:
        return "server_error"
    else:
        raise ValueError(f"unknown status code: {code}")
