def classify_status(code: int) -> str:
    """
    Classifies an HTTP status code into one of five categories:
    "informational", "success", "redirect", "client_error", or "server_error".

    Args:
        code: An integer representing the HTTP status code.

    Returns:
        A string indicating the category of the status code.

    Raises:
        ValueError: If the code is not within the valid range of 100-599.
    """
    if not isinstance(code, int):
        raise ValueError("Status code must be an integer.")

    if not (100 <= code <= 599):
        raise ValueError("Status code must be between 100 and 599 (inclusive).")

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
        # This case should theoretically not be reached due to the initial validation,
        # but included for completeness and defensive programming.
        raise ValueError("Status code is out of expected classification ranges.")
