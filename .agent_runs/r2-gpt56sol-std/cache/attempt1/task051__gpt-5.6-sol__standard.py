def normalize_case(text: str) -> str:
    """Lowercase text and capitalize the first alphabetic character of each sentence."""
    result: list[str] = []
    sentence_start = True

    for char in text.lower():
        if sentence_start and char.isalpha():
            result.append(char.upper())
            sentence_start = False
        else:
            result.append(char)

        if char in ".!?":
            sentence_start = True

    return "".join(result)
