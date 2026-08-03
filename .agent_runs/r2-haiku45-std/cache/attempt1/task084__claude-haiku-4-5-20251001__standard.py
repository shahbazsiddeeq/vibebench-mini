def classify_status(code):
    """
    Classify HTTP status codes into categories.
    
    Args:
        code: An integer HTTP status code
        
    Returns:
        A string representing the status category:
        - "informational" for 100-199
        - "success" for 200-299
        - "redirect" for 300-399
        - "client_error" for 400-499
        - "server_error" for 500-599
        
    Raises:
        ValueError: If code is outside the range 100-599
    """
    if code < 100 or code > 599:
        raise ValueError(f"Status code {code} is outside the valid range 100-599")
    
    if 100 <= code < 200:
        return "informational"
    elif 200 <= code < 300:
        return "success"
    elif 300 <= code < 400:
        return "redirect"
    elif 400 <= code < 500:
        return "client_error"
    else:  # 500 <= code < 600
        return "server_error"
