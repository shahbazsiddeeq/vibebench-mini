"""HTTP status code classification utilities."""


_STATUS_CLASSES = {
    1: "informational",
    2: "success",
    3: "redirect",
    4: "client_error",
    5: "server_error",
}


def classify_status(code: int) -> str:
    """Return the category for an HTTP status code from 100 through 599.

    Raises:
        TypeError: If ``code`` is not an integer.
        ValueError: If ``code`` is outside the valid range.
    """
    if isinstance(code, bool) or not isinstance(code, int):
        raise TypeError("status code must be an integer")
    if not 100 <= code <= 599:
        raise ValueError("status code must be between 100 and 599")

    return _STATUS_CLASSES[code // 100]
