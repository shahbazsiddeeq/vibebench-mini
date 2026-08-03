# src/solution.py

def word_wrap(text: str, width: int) -> list:
    if not isinstance(text, str) or not isinstance(width, int):
        raise ValueError("Invalid input types: text must be a string and width must be an integer.")
    
    if width <= 0:
        raise ValueError("Width must be a positive integer.")
    
    words = text.split()
    
    # Check if any single word exceeds the specified width
    for word in words:
        if len(word) > width:
            raise ValueError("A single word exceeds the specified width.")
    
    lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + len(current_line) > width:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines
