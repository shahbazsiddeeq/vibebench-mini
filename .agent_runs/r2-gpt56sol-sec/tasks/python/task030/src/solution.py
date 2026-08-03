"""Unicode-aware word frequency counter."""


def word_freq(text: str) -> dict[str, int]:
    """Return counts of lowercase words in *text*.

    A word is a maximal sequence of Unicode letters and digits.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    frequencies: dict[str, int] = {}
    current: list[str] = []

    for character in text:
        if character.isalpha() or character.isdigit():
            current.append(character)
        elif current:
            word = "".join(current).lower()
            frequencies[word] = frequencies.get(word, 0) + 1
            current.clear()

    if current:
        word = "".join(current).lower()
        frequencies[word] = frequencies.get(word, 0) + 1

    return frequencies
