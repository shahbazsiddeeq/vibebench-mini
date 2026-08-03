from __future__ import annotations


def word_wrap(text: str, width: int) -> list[str]:
    if not text.strip():
        return []
    words = text.split()
    for w in words:
        if len(w) > width:
            raise ValueError(f"word '{w}' exceeds width {width}")
    lines = []
    current = ""
    for w in words:
        if not current:
            current = w
        elif len(current) + 1 + len(w) <= width:
            current += " " + w
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines
