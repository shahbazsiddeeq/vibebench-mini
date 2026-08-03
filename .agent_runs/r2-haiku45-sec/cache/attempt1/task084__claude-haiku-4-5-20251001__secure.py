def classify_status(code):
    """
    Classify HTTP status codes into categories.
    
    Args:
        code: An integer HTTP status code
        
    Returns:
        A string representing the status category:
        - "informational" for codes 100-199
        - "success" for codes 200-299
        - "redirect" for codes 300-399
        - "client_error" for codes 400-499
        - "server_error" for codes 500-599
        
    Raises:
        ValueError: If code is not an integer in the range 100-599
    """
    # Validate input type
    if not isinstance(code, int) or isinstance(code, bool):
        raise ValueError(f"Status code must be an integer, got {type(code).__name__}")
    
    # Validate input range
    if code < 100 or code > 599:
        raise ValueError(f"Status code must be between 100 and 599, got {code}")
    
    # Classify based on range
    if code < 200:
        return "informational"
    elif code < 300:
        return "success"
    elif code < 400:
        return "redirect"
    elif code < 500:
        return "client_error"
    else:
        return "server_error"
