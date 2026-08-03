# src/solution.py

def classify_status(code):
    if not (100 <= code <= 599):
        raise ValueError("Status code must be between 100 and 599.")
    
    if 100 <= code < 200:
        return "informational"
    elif 200 <= code < 300:
        return "success"
    elif 300 <= code < 400:
        return "redirect"
    elif 400 <= code < 500:
        return "client_error"
    elif 500 <= code < 600:
        return "server_error"
