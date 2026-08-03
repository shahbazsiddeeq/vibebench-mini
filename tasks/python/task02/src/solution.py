def reverse_words(s: str) -> str:
    words = s.strip().split()
    return " ".join(reversed(words))
