"""
src/solution.py

A small, security-conscious utility module for classifying HTTP status
codes into their broad category.

The public function `classify_status` performs strict input validation
to ensure it only accepts well-formed integer HTTP status codes in the
valid range (100-599), and never executes arbitrary code or trusts
external input blindly.
"""

from typing import Final

# Valid HTTP status code range as per RFC 7231 / common conventions.
_MIN_STATUS_CODE: Final[int] = 100
_MAX_STATUS_CODE: Final[int] = 599


def classify_status(code: int) -> str:
    """
    Classify an HTTP status code into one of the standard categories.

    Args:
        code: An integer HTTP status code (100-599 inclusive).

    Returns:
        One of: "informational", "success", "redirect",
        "client_error", "server_error".

    Raises:
        ValueError: If `code` is not an integer, or is outside the
            valid range of 100-599.
    """
    # Strict type validation: reject bools (which are ints in Python)
    # and any non-integer types to avoid subtle bugs or injection of
    # unexpected objects.
    if isinstance(code, bool) or not isinstance(code, int):
        raise ValueError("HTTP status code must be an integer.")

    if not (_MIN_STATUS_CODE <= code <= _MAX_STATUS_CODE):
        raise ValueError(
            f"HTTP status code must be between {_MIN_STATUS_CODE} "
            f"and {_MAX_STATUS_CODE}, inclusive."
        )

    if 100 <= code < 200:
        return "informational"
    if 200 <= code < 300:
        return "success"
    if 300 <= code < 400:
        return "redirect"
    if 400 <= code < 500:
        return "client_error"
    # Remaining valid range is 500-599.
    return "server_error"
