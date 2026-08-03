def normalize_case(text: str) -> str:
    text = text.lower()
    result = list(text)
    capitalize_next = True
    for i, ch in enumerate(result):
        if capitalize_next and ch.isalpha():
            result[i] = ch.upper()
            capitalize_next = False
        elif ch in '.!?':
            capitalize_next = True
    return ''.join(result)
