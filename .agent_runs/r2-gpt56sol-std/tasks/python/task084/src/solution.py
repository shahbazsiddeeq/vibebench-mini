"""Utilities for classifying HTTP status codes."""


def classify_status(code: int) -> str:
    """Return the HTTP status class for a code between 100 and 599."""
    if not isinstance(code, int) or isinstance(code, bool) or not 100 <= code <= 599:
        raise ValueError("HTTP status code must be an integer between 100 and 599")

    return {
        1: "informational",
        2: "success",
        3: "redirect",
        4: "client_error",
        5: "server_error",
    }[code // 100]
