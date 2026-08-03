def classify_status(code):
    if not isinstance(code, int) or isinstance(code, bool):
        raise ValueError("Status code must be an integer")
    if code < 100 or code > 599:
        raise ValueError("Status code out of range (100-599)")
    if 100 <= code < 200:
        return "informational"
    elif 200 <= code < 300:
        return "success"
    elif 300 <= code < 400:
        return "redirect"
    elif 400 <= code < 500:
        return "client_error"
    else:
        return "server_error"
