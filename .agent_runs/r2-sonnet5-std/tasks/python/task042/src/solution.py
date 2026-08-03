def word_wrap(text, width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        if len(word) > width:
            raise ValueError(f"Word '{word}' exceeds width {width}")

        if not current:
            current = word
        elif len(current) + 1 + len(word) <= width:
            current += " " + word
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines
