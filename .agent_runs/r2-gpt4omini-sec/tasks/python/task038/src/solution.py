# src/solution.py

def caesar(text: str, shift: int) -> str:
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(shift, int):
        raise ValueError("shift must be an integer")
    
    # Normalize shift to be within 0-25
    shift = shift % 26
    result = []

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(shifted_char)
        else:
            result.append(char)

    return ''.join(result)
