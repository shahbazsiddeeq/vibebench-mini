def normalize_case(text: str) -> str:
    if not text:
        return ""

    result_chars = list(text.lower())
    capitalize_next = True

    for i, char in enumerate(result_chars):
        if capitalize_next and char.isalpha():
            result_chars[i] = char.upper()
            capitalize_next = False
        elif char in ('.', '!', '?'):
            capitalize_next = True
            
    return "".join(result_chars)
