def classify_status(code):
    """
    Classify HTTP status codes into categories.
    
    Args:
        code: An integer HTTP status code
        
    Returns:
        A string classification: "informational", "success", "redirect",
        "client_error", or "server_error"
        
    Raises:
        ValueError: If code is outside the range 100-599
    """
    if code < 100 or code > 599:
        raise ValueError(f"Status code {code} is outside valid range 100-599")
    
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
