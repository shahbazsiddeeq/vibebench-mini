def word_wrap(text, width):
    if width < 1:
        raise ValueError("Width must be at least 1")

    words = text.split()
    if any(len(word) > width for word in words):
        raise ValueError("A word exceeds the given width")

    lines = []
    current_line = []

    for word in words:
        if current_line:
            # Check if adding the next word exceeds the width
            if len(' '.join(current_line + [word])) <= width:
                current_line.append(word)
            else:
                # Add the current line to lines and start a new line
                lines.append(' '.join(current_line))
                current_line = [word]
        else:
            # Start a new line with the current word
            current_line.append(word)

    # Add the last line if it exists
    if current_line:
        lines.append(' '.join(current_line))

    return lines
