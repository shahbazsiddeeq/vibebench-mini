def word_wrap(text, width):
    if any(len(word) > width for word in text.split()):
        raise ValueError("A single word exceeds the specified width.")

    lines = []
    current_line = []

    for word in text.split():
        if len(word) > width:
            raise ValueError("A single word exceeds the specified width.")
        
        if sum(len(w) for w in current_line) + len(current_line) + len(word) > width:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)

    if current_line:
        lines.append(' '.join(current_line))

    return lines
